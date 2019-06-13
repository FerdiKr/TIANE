### Frontend-Requests "GET"
| URL          | Description |
|--------------|-------------|
| `/` or `/index` | On unconfigured setups this endpoint points to `/setup`. Otherwise it shows an overview of all services and configurations. |
| `/setup` | This is the welcome-page for the first setup-Assistant. It just takes the user to the `/setup_2`-page. |
| `/setup_2` | all modules in the services.json-file are listed and checked if they are installed correctly. |
| `/setup_3` | "Setup" complete - Redirect-Menu to configure the server, users and rooms. |
| `/setupServer` | |
| `/setupUser` | |
| `/setupRoom` | |

### Backend-Requets

* [x] `/api/installer/listPackages/<extended>` (extended=True/False)
* [x] `/api/installer/getStatus`
* [x] `/api/installer/startInstallation/<packageName>`
* [ ] `/api/setup/prerequesites`
* [x] `/api/writeConfig/server`
* [x] `/api/writeConfig/user`
* [ ] `/api/writeConfig/room`
* [x] `/api/loadConfig/user/<userName>`
* [ ] `/api/uploadSpeech/<userName>`

* [x] `/api/server/list/<action>` (action=room, users, modules, telegram)
* [x] `/api/server/<action>` (action=status, start, stop, version)
* [x] `/api/module/list` (see `/api/server/list/modules`)
* [ ] `/api/module/<modName>/<action>` (action=load, unload, status)
