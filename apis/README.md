# Setting Up Nodemon for Go Development

## Install Nodemon

Once you have Node.js and npm installed, you can install Nodemon globally using npm. Open your terminal and run:

```bash
npm install -g nodemon
```

## Run the Command

After you have installed Go, Node.js, and Nodemon, you can run your command. Make sure you are in the directory where your `main.go` file is located, then run:

```bash
nodemon --exec go run main.go --ext go
```

## What This Command Does

This command sets up a development environment that allows you to automatically refresh your Go server whenever you save changes to your code. It's perfect for development mode, as it eliminates the need to manually stop and restart your server after each modification.

### Breakdown:
- `nodemon`: Monitors your files for changes
- `--exec go run main.go`: Executes your Go program
- `--ext go`: Watches for changes in files with the `.go` extension

By using this setup, you can focus on writing code without the hassle of constant manual server restarts. Simply save your changes, and Nodemon will automatically reload your application, making your development process smoother and more efficient.