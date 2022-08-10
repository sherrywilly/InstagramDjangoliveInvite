const express = require('express');
const path = require('path');
const app = express()
const demo = require('./router/demo');
const bodyParser = require('body-parser');


// app.use(express.json()) // for json
app.use(bodyParser.json()); ; // for parsing application/json
app.use(express.urlencoded({ extended: true }))
app.use(express.static("view"))
app.use('/demo', demo)

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
    console.log(`server is running on port : ${PORT}`)
})
