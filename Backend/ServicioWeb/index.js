const express = require('express')
const fileUpload = require('express-fileupload')
const mongodb = require('mongodb')
const fs = require('fs')

const app = express()
const router = express.Router()
const mongoClient = mongodb.MongoClient
const binary = mongodb.Binary

router.get("/", (req, res) => {
    mongoClient.
    res.json()
})

router.get("/download", (req, res) => {
    getFiles(res)
})

app.use(fileUpload())

router.post("/upload", (req, res) => {
    let file = { user: 0, file: binary(req.body.image) }
    insertFile(file, res)
})

function insertFile(file, res) {
    mongoClient.connect('mongodb://localhost:27017', { useNewUrlParser: true }, (err, client) => {
        if (err) {
            return err
        }
        else {
            let db = client.db('bacteriaclassifier')
            let collection = db.collection('images')
            try {
                collection.insertOne(file)
                console.log('File Inserted')
            }
            catch (err) {
                console.log('Error while inserting:', err)
            }
            client.close()
            res.redirect('/')
        }

    })
}

app.use("/", router)

app.listen(3000, () => console.log('Started on 3000 port'))