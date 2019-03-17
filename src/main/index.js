import {
  app,
  BrowserWindow
} from 'electron'
import path from 'path'

/**
 * Set `__static` path to static files in production
 * https://simulatedgreg.gitbooks.io/electron-vue/content/en/using-static-assets.html
 */
if (process.env.NODE_ENV !== 'development') {
  global.__static = require('path').join(__dirname, '/static').replace(/\\/g, '\\\\')
}

let mainWindow
let pythonProcess = null
let pythonPort = null

const PY_DIST_FOLDER = 'pyDist'
const PY_FOLDER = 'python'
const PY_MODULE = 'main' // without .py suffix

const guessPackaged = () => {
  const fullPath = path.join(__dirname, PY_DIST_FOLDER)
  return require('fs').existsSync(fullPath)
}

const getScriptPath = () => {
  if (!guessPackaged()) {
    return path.join(__dirname, PY_FOLDER, PY_MODULE + '.py')
  }
  if (process.platform === 'win32') {
    return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE, PY_MODULE + '.exe')
  }
  return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE, PY_MODULE)
}


const winURL = process.env.NODE_ENV === 'development' ?
  `http://localhost:9080` :
  `file://${__dirname}/index.html`

function createWindow() {
  mainWindow = new BrowserWindow({
    height: 563,
    useContentSize: true,
    width: 1000
  })
  // mainWindow.maximize()
  mainWindow.loadURL(winURL)

  mainWindow.on('closed', () => {
    mainWindow = null
  })
}

function selectPort() {
  pythonPort = 1122
  return pythonPort
}

const createPythonProcess = () => {
  let script = getScriptPath()
  let port = '' + selectPort()

  if (guessPackaged()) {
    // pythonProcess = require('child_process').execFile(script, [port])
    let script = path.join(__dirname, '../python/', 'main.py')
    pythonProcess = require('child_process').spawn('python', [script, port])
    console.log('child execution success on port ' + port)
  } else {
    pythonProcess = require('child_process').spawn('python', [script, port])
    console.log('child process success on port ' + port)
  }

  // if (pythonProcess != null) {
  //   //console.log(pyProc)
  //   console.log('child process success on port ' + port)
  // }
}

// function createPythonProcess() {
//   let port = '' + selectPort()
//   let script = path.join(__dirname, '../python/', 'main.py')
//   pythonProcess = require('child_process').spawn('python', [script, port])
//   if (pythonProcess != null) {
//     console.log('child process success')
//   }
// }

function exitPythonProcess() {
  console.log('asd')
  pythonProcess.kill()
  pythonProcess = null
  pythonPort = null
}

app.on('ready', createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow()
  }
})

app.on('ready', createPythonProcess)
app.on('quit', exitPythonProcess)

/**
 * Auto Updater
 *
 * Uncomment the following code below and install `electron-updater` to
 * support auto updating. Code Signing with a valid certificate is required.
 * https://simulatedgreg.gitbooks.io/electron-vue/content/en/using-electron-builder.html#auto-updating
 */

/*
import { autoUpdater } from 'electron-updater'

autoUpdater.on('update-downloaded', () => {
  autoUpdater.quitAndInstall()
})

app.on('ready', () => {
  if (process.env.NODE_ENV === 'production') autoUpdater.checkForUpdates()
})
 */