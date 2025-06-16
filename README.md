# Fongnosudo

This is my first blog website, made by with me with a lot of help from AI, especially Gemini by Google. Thank you, Gemini!

This project uses Python Flask for the backend and Vuejs for the frontend

# How to run project ?



Clone the project

```bash
  git clone https://github.com/DooxFonggg/fongnosudo.git
```
```bash
  cd /fongnosudo/fongnosudo-fe
  cp .env.example .env
```

```bash
  export $(grep -v '^#' .env | xargs)
```

Then edit .env file to match your setting.

```bash
  cd /fongnosudo/scripts
  cp .env.example .env
```
Edit .env file to match your setting. Then run the start.sh file.
```bash
  export $(grep -v '^#' .env | xargs)
```
```bash
  bash start.sh
```
After running start.sh, if it shows this, congratulations, project has started successfully !
```bash
  🚀 Starting Fongnosudo Blog...
[+] Running 4/4
 ✔ Network scripts_fongnosudo-network  Created                                                                              0.1s
 ✔ Container fongnosudo-postgres       Healthy                                                                             10.8s
 ✔ Container fongnosudo-backend        Started                                                                             11.1s
 ✔ Container fongnosudo-frontend       Started                                                                             11.5s
✅ Services started!
📊 Backend: http://127.0.0.1/api/
🌐 Frontend: http://127.0.0.1/

Run 'docker-compose logs -f' to see logs
```
Stop the project and check it logs using the stop.sh and logs.sh 

```bash
  bash stop.sh
  bash logs.sh
```

## Authors

- [@DooxFonggg](https://github.com/DooxFonggg)