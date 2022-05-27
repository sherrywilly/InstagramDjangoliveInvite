const express = require('express');
const path = require('path');
const axios = require('axios');
const { response } = require('express');
const router = express.Router();
const request = require('request');
var url = require('url');
var https = require('https');
var HttpsProxyAgent = require('https-proxy-agent');

// const HttpAgent = new HttpsProxyAgent('https://sKMty7:JUsYZ2@45.145.57.224:10524');
// const axios = require('axios').create({
//     httpAgent: HttpAgent
// });

const Pool = require('pg').Pool
const pool = new Pool({
  user: 'admin',
  host: 'db',
  database: 'postgres',
  password: 'pwd',
  port: 5432,
})


router.get('/', (req, res) => {
    res.send({
        "status": "ok",
        "message": "Welcome to the API"
    })
}
)


router.post('/', (req, res) => {
    let cookie = req.body.cookie;
    let data = req.body.data;
    let proxy = req.body.proxy;
    let ig_id = req.body.ig_id
     
    if (!cookie || cookie == '') {
        res.send({
            "status": "error",
            "message": "cookie is required"
        });
        return;
    }
    if (!data || data == '' || data == null || data == undefined) {
        res.send({
            "status": "error",
            "message": "data is required"
        });
        return;
    }
    // check data is an array
    if (!Array.isArray(data)) {
        res.send({
            "status": "error",
            "message": "data is not an array"
        });
        return;
    }
    let format_cookie = ''
    for (let key in cookie) {
        format_cookie += key + '=' + cookie[key] + ';'
    }
    let ua = 'Instagram 231.0.0.18.113 Android (11\\/3.3.1; 120; 480x800; samsung; GT-N7000; GT-N7000; smdkc210; en_US)'

    let axiosConfig = {
        headers: {
            'Cookie': format_cookie,
            'User-Agent': 'Instagram 231.0.0.18.113 Android (11\\/3.3.1; 120; 480x800; samsung; GT-N7000; GT-N7000; smdkc210; en_US)',
            'Content-Type': 'application/json'
        }
    }
    let body;
    for (let i = 0; i < data.length; i++) {
        let url = 'https://i.instagram.com/api/v1/story_interactions/send_story_like/'
        let ua = 'Instagram 231.0.0.18.113 Android (30/11; 480dpi; 1080x2132; realme; RMX1921; RMX1921; qcom; en_GB; 321039152)'
        let postDate = {
            "media_id": data[i],
            "container_module": "reel_feed_timeline"
        }
        console.log(proxy)
        let options = {
            url: url,
            method: 'POST',
            headers: {
                'Cookie': format_cookie,
                'User-Agent': ua,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(postDate),
           proxy: proxy

        }
        request(options, function (error, response, body) {
            if (error) {
                console.log(error);
                console.log(" Error in request ");
            }
            // console.log(body);
            // write response to a file
            // console the body content
            // console.log(body);

            try{
            console.log(response.body);


            
            let datetime = new Date().toISOString().replace(/T/, ' ').replace(/\..+/, '');


            pool.query('INSERT INTO core_status (ig_id_id,status,comment,response,datetime) VALUES ($1, $2,$3,$4,$5)', [ig_id,"Success",postDate,response.body,datetime], (error, results) => {
                if (error) {
                  throw error
                }
            })
        }
        catch(err){
            let datetime = new Date().toISOString().replace(/T/, ' ').replace(/\..+/, '');
            pool.query('INSERT INTO core_status (ig_id_id,status,comment,response,datetime) VALUES ($1, $2,$3,$4,$5)', [ig_id,"Fail",postDate,err,datetime], (error, results) => {
                
            })
        }
            // body = response
            // if (response.status == 'ok') {
            //     console.log('success')
            // } else {
                
                var fs = require('fs');
                var stream = fs.createWriteStream("my_file.txt");
                stream.once('open', function (fd) {
                    try{
                    stream.write(body)
                    }
                    catch{
                        console.log(response)
                    }
                })
                // console.log("ERROR ENDS")
            // }
        });

    }


    res.json({
        "status": "ok"
    })

}
)
module.exports = router;