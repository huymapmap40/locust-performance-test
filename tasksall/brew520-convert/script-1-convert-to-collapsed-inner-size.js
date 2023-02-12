const fs = require('fs');
const { keywords } = require('./constants');

async function main(){
    keywords.forEach(function(keyword){
      console.log(`converting: ${keyword}`)
        let json = JSON.parse(fs.readFileSync(`./original/${keyword}.json`));
        json.body[1]['collapse']['inner_hits']['size'] = 100;
        fs.writeFileSync(`./original-convet-to-collapsed-inner-size/${keyword}.json`, JSON.stringify(json));
    })
}

main();
