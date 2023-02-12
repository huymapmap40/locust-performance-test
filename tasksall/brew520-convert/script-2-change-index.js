const fs = require('fs');
const { keywords } = require('./constants');

async function main(){
    keywords.forEach(function(keyword){
      console.log(`converting: ${keyword}`)
        let json = JSON.parse(fs.readFileSync(`./original/${keyword}.json`));
        json.body[0].index = "au-raw-product-data-loadtest";
        json.body[2].index = "au-raw-product-data-loadtest"; 
        fs.writeFileSync(`./original-with-test-index/${keyword}.json`, JSON.stringify(json));
    })
}

main();
