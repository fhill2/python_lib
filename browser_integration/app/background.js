let searchingForNotesFolderId = browser.bookmarks
  .search({ title: "notes" })
  .then(
    (items) => {
      for (item of items) {
        if (item.type == "folder") {
          return item.id;
        }
      }
      console.log("failed to set notes folder Id");
    },
    (error) => {
      console.log(
        "failed searching for notes folder - does the folder exist?? - " + error
      );
    }
  );

let searchingForStarsFolderId = browser.bookmarks
  .search({ title: "stars" })
  .then(
    (items) => {
      for (item of items) {
        if (item.type == "folder") {
          return item.id;
        }
      }
      console.log("failed to set stars folder Id");
    },
    (error) => {
      console.log(
        "failed searching for stars folder - does the folder exist?? - " + error
      );
    }
  );

Promise.allSettled([searchingForNotesFolderId, searchingForStarsFolderId])
  .then((promises) => {
    notesFolderId = promises[0].value;
    starsFolderId = promises[1].value;

    let port = browser.runtime.connectNative("browser_integration");

    function sendSuccess(message) {
      console.log("sending success msg: " + message);
      port.postMessage({
        type: "success",
        data: message,
      });
    }

    function sendError(message) {
      console.log("sending error msg");
      port.postMessage({
        type: "error",
        data: message,
      });
    }

    function removeBookmark(message) {
      browser.bookmarks.remove(message.id).then(
        () => {
          sendSuccess("Succesfully removed bookmark"); // onRemoved
        },
        (error) => {
          sendError(`bookmark failed to remove: ${error}`); // onRejected
        }
      );
    }

    function createBookmark(message, parentFolderId) {
      browser.bookmarks
        .create({
          title: message.title,
          url: message.url,
          parentId: parentFolderId,
        })
        .then(
          (bookmark) => {
            sendSuccess("Succesfully created bookmark: " + bookmark.url); // onCreated
          },
          (error) => {
            console.log(error);
            sendError(`bookmark failed to create: ${error}`); // onRejected
          }
        );
      // also create tags for the bookmark
      if (message.tags) {
        setTags(message.url, message.tags);
      }
    }

    function updateBookmark(message) {
      console.log("updating bookmark..");
      if (message.title) {
        browser.bookmarks.update(message.id, { title: message.title });
      }
      if (message.tagsToCreate) {
        console.log("creating tags", message.tagsToCreate);
        setTags(message.url, message.tagsToCreate);
      }
      if (message.tagsToRemove) {
        console.log("removing tags", message.tagsToRemove);
        removeTags(message.url, message.tagsToRemove);
      }
      // TODO: do not send success if update fails (cba atm)
      console.log("successfully updated bookmark!!");
      sendSuccess("updated Bookmark: " + message.url);
    }

    port.onMessage.addListener((res) => {
      console.log("Message Received: ", res);
      // sendSuccess after every received message otherwise python client hangs
      // res = JSON.parse(res)

      switch (res.data.command) {
        case "preview":
          preview(res.data.message);
          break;
        case "test":
          sendSuccess("hello world");
          break;
        case "create_notes_bookmark":
          createBookmark(res.data.message, notesFolderId);
          break;
        case "create_stars_bookmark":
          createBookmark(res.data.message, starsFolderId);
          break;
        case "remove_bookmark":
          removeBookmark(res.data.message);
          break;
        case "update_bookmark":
          updateBookmark(res.data.message);
          break;
        case "get_notes_bookmarks":
          getBookmarks(notesFolderId);
          break;
        case "get_stars_bookmarks":
          getBookmarks(starsFolderId);
          break;
      }
    });

    function handleBookmarks(bookmarksList) {
      allTagPromises = [];
      for (const mark of bookmarksList) {
        allTagPromises.push(
          browser.experiments.tags.getTagsForURI(mark.url).then((values) => {
            return values;
          })
        );
      }

      Promise.allSettled(allTagPromises).then((promises) => {
        // console.log("at promise settled", values)
        bookmarks = {};
        for (const mark of bookmarksList) {
          bookmarks[mark.url] = {
            url: mark.url,
            title: mark.title,
            id: mark.id,
          };
        }

        for (promise of promises) {
          bookmarks[promise.value.url].tags = promise.value.tags;
        }

        sendSuccess(bookmarks);
      });
    }

    function getBookmarks(folderId) {
      console.log(folderId);
      // get all bookmarks inside of a bookmark subfolder
      browser.bookmarks.getSubTree(folderId).then(
        (bookmarkItems) => {
          handleBookmarks(bookmarkItems[0].children);
        },
        (error) => {
          console.log(`An error: ${error}`);
        }
      );
    }

    function setTags(url, newTags) {
      // does not overwrite existing tags
      browser.experiments.tags.tagURI(url, newTags).then(
        (URI, newTags) => {
          console.log("tag creation successful", URI, newTags);
        },
        (error) => {
          console.log("tag creation failed: " + error);
        }
      );
    }

    function removeTags(url, tagsToRemove) {
      // does not overwrite existing tags - only if included in tags to remove
      browser.experiments.tags.untagURI(url, tagsToRemove).then(
        (url, tagsRemoved) => {
          console.log("tag removal successful", url, tagsRemoved);
        },
        (error) => {
          console.log("failed to remove tags: " + error.message);
        }
      );
    }

    // ============= PREVIEWER FUNCTIONS ==============
    manager = {};
    manager.winIds = {};

    function createNewTab(url, targetTab) {
      console.log(url);
      browser.tabs.create(
        {
          url: url,
          openerTabId: targetTab.id,
          windowId: targetTab.windowId,
        },
        function onCreateTab(tab) {
          manager.winIds[tab.windowId] = tab.id;
        }
      );
    }

    // targetTab = the tab to the left of the live preview
    function updateOrCreatePreviewTab(url, targetTab) {
      c_tab = manager.winIds[targetTab.windowId];
      c_tab
        ? browser.tabs.update(targetTab.id, { url: url })
        : createNewTab(url, targetTab);
    }

    // chrome window top left width height are relative to a screen, so that data can't tell you what screen/monitor the window is on
    // i cant find any screen / window / tab method that can link one of these to the monitor it exists on
    // so, the current implementation:
    // if window id is found in the passed in title, it uses that, otherwise it iterates all tab titles until it finds a match with the passed in title
    // TODO: if regex doesnt match, and there are 2 TABS WITH THE SAME TITLE FOUND..compares browser's visible window dimensions (passed in from native messaging) with the width and height dimensions of all chrome windows, and picks closest match
    // TODO: modify this - if regex does or does not match, suppprt 2 browser windows on the same screen, and choose one closest in distance

    function preview(message) {
      browser.windows
        .getAll({
          populate: true,
          windowTypes: ["normal"],
        })
        .then(
          (windows) => {
            for (const window of windows) {
              if (window.id == message.id) {
                browser.tabs.query({ windowId: window.id }).then(
                  (tabs) => {
                    console.log("GET ALL TABS RAN");
                    updateOrCreatePreviewTab(message.url, tabs.pop());
                  },
                  (error) => {
                    console.log(error);
                  }
                );
              }
            }
            sendSuccess("Succesfully previewed: " + message.url);
          },
          (error) => {
            console.log(error);
          }
        );
    }

    // for debugging
  })
  .catch((error) => {
    console.log(error);
  }); // Promise.allSettled
// Whole extension wrapped in promise.Settled callback - so promnesiaFolderId is set before extension works

// ========== PREVIEW EVENT HANDLERS ==========
browser.tabs.onCreated.addListener(function (activeInfo) {
  setTimeout(() => {
    updateWindowTitles();
  }, 300);
});

browser.windows.onCreated.addListener(function (window) {
  updateWindowTitles();
});

function updateWindowTitles() {
  browser.windows
    .getAll({
      populate: true,
      windowTypes: ["normal"],
    })
    .then(
      (windows) => {
        for (const window of windows) {
          console.log(window);
          browser.windows.update(window.id, {
            titlePreface: String(window.id) + " ",
          });
        }
      },
      (error) => {
        console.log(error);
      }
    );
}

// as browser.runtime.onStartup callback does not work, probably due to loading a temporary extension
// setTimeout(() => {
// updateWindowTitles();
// }, 400);

// https://stackoverflow.com/a/27787423
window.onload = function () {
  setTimeout(() => {
    updateWindowTitles();
  }, 300);
};

// TEST
function newTabPls() {
  console.log("new tab trig");
  browser.tabs.create(
    {
      url: "file:///home/f1/Downloads",
      // url: "https://google.com",
    },
    function onCreateTab(tab) {
      manager.winIds[tab.windowId] = tab.id;
    }
  );
}
browser.browserAction.onClicked.addListener(newTabPls);

////// OLD

// if (changeInfo.title && !changeInfo.title.endsWith(tab.windowId)) {
// console.log(changeInfo);
// newTitle = tab.title + " - " + tab.windowId;
// code = "document.title = '" + newTitle + "'";
// browser.tabs.executeScript(tabId, { code: code });
// }
// function preview(message) {
//   console.log("preview trig");
//   title = message.target.visible[0].title;
//   match = title.match(/-\s(\d{9})\s-/);
//   console.log("title: " + title);
//   if (match) {
//     // all visible current workspace firefox window titles are sent to browser
//     // if the list of firefox window titles match with the names of the internal windows
//     winId = parseInt(match[1]);
//     console.log("MATCHED REGEX: " + winId);
//     // find target tab
//     console.log(winId);
//     browser.tabs.getAllInWindow(winId, function (tabs) {
//       updateOrCreatePreviewTab(message.url, tabs.pop());
//     });
//   } else {
//     browser.tabs.query({}, function (tabs) {
//       tabs.forEach(function (tab) {
//         console.log(tab);
//         if (title.startsWith(tab.title)) {
//           console.log("MATCHED ITERATION: " + tab);
//           updateOrCreatePreviewTab(message.url, tab);
//         }
//       });
//     });
//   }
// }
