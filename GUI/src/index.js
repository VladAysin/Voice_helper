const { app, BrowserWindow, Tray, Menu,  } = require('electron');
const path = require('path');
const axios = require('axios');
const WebSocket = require('ws');
const ReconnectingWebSocket = require('reconnecting-websocket');
const instance = axios.create({
  baseURL: 'http://something.com',
  timeout: 1000,
})
let temp;

const client = new ReconnectingWebSocket('ws://10.11.17.2:22150', [], {WebSocket: WebSocket});
client.onopen = () => {
  client.send('hello from client')
};
client.onmessage = (e) => {
  console.log('received data: ', e.data);
};

client.onerror = (e) => {
  console.error(e);
};

client.onclose = () => {
  console.log('websocket closed');
};



instance.get('https://jsonplaceholder.typicode.com/todos').then(r => {
  temp = r.data;
  // console.log(temp);
})

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require('electron-squirrel-startup')) { // eslint-disable-line global-require
  app.quit();
}
let tray;
const createWindow = () => {
  const createTray = () => {
    let appIcon = new Tray(path.join(__dirname, "Untitled-1.ico"));
    const contextMenu = Menu.buildFromTemplate([
      {
        label: 'Show', click: function () {
          mainWindow.show();
        }
      },
      {
        label: 'Exit', click: function () {
          app.isQuiting = true;
          app.quit();
        }
      }
    ]);

    appIcon.on('double-click', function (event) {
      mainWindow.show();
    });
    appIcon.setToolTip('Assistant');
    appIcon.setContextMenu(contextMenu);
    return appIcon;
  }
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 400,
    height: 700,
  });
  mainWindow.setMenuBarVisibility(false);
  // mainWindow.webContents.openDevTools();
  // and load the index.html of the app.
  mainWindow.loadFile(path.join(__dirname, 'index.html'));
  mainWindow.on('minimize',function(event){
    event.preventDefault();
    mainWindow.hide();
    tray = createTray();
  });
  mainWindow.on('restore', (event) => {
    mainWindow.show();
    tray.destroy();
  })
};

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow);

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and import them here.
