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

router.get('/', (req, res) => {

    // let cookie = req.params.Cookie;
    // var cookie = { "mid": "YokcTAABAAFQ9GHLUgjHhPgcOoSG", "rur": "NCG", "csrftoken": "HY30xuKGOZEQ3KjJZBtQNEcMSs8YrTiB", "sessionid": "9657000400%3AhmSH5hJhV0UO5g%3A1", "ds_user_id": "9657000400" }
    // let format_cookie = ''
    // for (let key in cookie) {
    //     format_cookie += key + '=' + cookie[key] + ';'
    // }
    // // let headers = {
    // //     'Content-Type': 'application/Json',
    // //     'user-agent': ua,
    // //     'Cookie': format_cookie,
    // // }
    // let proxy = 'http://sKMty7:JUsYZ2@45.145.57.224:10524'

    // var options = {
    //     'method': 'POST',
    //     'url': 'https://i.instagram.com/api/v1/story_interactions/send_story_like/',
    //     'proxy': proxy,
    //     'headers': {
    //         'Cookie': format_cookie,
    //         'User-Agent': 'Instagram 231.0.0.18.113 Android (11\\/3.3.1; 120; 480x800; samsung; GT-N7000; GT-N7000; smdkc210; en_US)',
    //         'Content-Type': 'application/json',
    //     },

    //     body: JSON.stringify({
    //         "media_id": "2446597535621417675",
    //         "container_module": "reel_feed_timeline"
    //     })

    // };
    // let axiosConfig = {
    //     headers: {
    //         'Cookie': format_cookie,
    //         'User-Agent': 'Instagram 231.0.0.18.113 Android (11\\/3.3.1; 120; 480x800; samsung; GT-N7000; GT-N7000; smdkc210; en_US)',
    //         'Content-Type': 'application/json'
    //     }
    // }
    // let postDate = {
    //     "media_id": "2446597535621417675",
    //     "container_module": "reel_feed_timeline"
    // }
    // let url = 'https://i.instagram.com/api/v1/story_interactions/send_story_like/'
    // axios.post(url, postDate, axiosConfig)
    //     .then(function (response) {
    //         console.log(response.data);
    //     })
    //     .catch(function (error) {
    //         console.log(error);
    //     });

    // axios with proxy
    // request(options, function (error, response, body) {
    //     if (error) throw new Error(error);
    //     console.log(body);
    // });
    res.send({
        "status": "ok"
    })
}
)


router.post('/', (req, res) => {
    let cookie = req.body.cookie;
    let data = req.body.data;
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
    // let headers = {
    //     'Content-Type': 'application/Json',
    //     'user-agent': ua,
    //     'Cookie': format_cookie,
    // }
    let axiosConfig = {
        headers: {
            'Cookie': format_cookie,
            'User-Agent': 'Instagram 231.0.0.18.113 Android (11\\/3.3.1; 120; 480x800; samsung; GT-N7000; GT-N7000; smdkc210; en_US)',
            'Content-Type': 'application/json'
        }
    }

    for (let i = 0; i < data.length; i++) {
        let url = 'https://i.instagram.com/api/v1/story_interactions/send_story_like/'
        let ua = 'Instagram 231.0.0.18.113 Android (11\\/3.3.1; 120; 480x800; samsung; GT-N7000; GT-N7000; smdkc210; en_US)'
        let postDate = {
            "media_id": data[i],
            "container_module": "reel_feed_timeline"
        }
        axios.post(url, postDate, axiosConfig)

            .then(function (response) {
                console.log(response.data);
            }
            )
            .catch(function (error) {
                console.log(error);
            }
            );

    }
    res.json({
        "status": "ok"
    })

}
)
module.exports = router;