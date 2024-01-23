
- [SOIL NUTRIENT](#soil-nutrient)
  - [Web](#web)
    - [ENV](#env)
  - [Database](#database)
  - [API](#api)

# SOIL NUTRIENT

The repository for the SOIL project.


## Web

Web container required a `soid` module.
To pull the submodule `git submodule update --init --recursive` or update to the latest module `git submodule update --recursive --remote`.
Then, the `web.Dockerfile` is ready to run the build.

### ENV

You need to connect to the database.
To do this, you will need to create an `db.env` file that will be shared between the `web` and `db` container.
Here is the `db.env` example.

```env
MARIADB_ROOT_PASSWORD=root
MARIADB_DATABASE=soil
MARIADB_USER=admin
MARIADB_PASSWORD=password
MARIADB_PORT=3306
MARIADB_HOSTNAME=db
```

Where the last two configurations (`PORT`, `HOSTNAME`) are used only in the `web` container.
This allowed the user to change the endpoint of the database.

Then, we will need another environment file `web.env`.

```env
ENABLE_DEBUG=true
IP_URL=http://localhost:9000
ENCRYPTION_KEY=thekey_gofigure
```

They consist of the sensitive configuration of the web. 



## Database

We have databack up in [Google Drive](https://drive.google.com/drive/folders/1sPbm_ARJPKNeB_Nc7WsEeeXONijqwDXH?usp=share_link)

## API

The API is the container serving the FastAPI project for predicting nutrients in the soil.