const fs = require('fs');
const { keywords } = require('./constants');

async function main(){
    keywords.forEach(function(keyword){
      console.log(`converting: ${keyword}`)
        let json = JSON.parse(fs.readFileSync(`./original/${keyword}.json`));
        delete json.body[1].aggs
        fs.writeFileSync(`./original-remove-aggs/${keyword}.json`, JSON.stringify(json));
    })
}

main();
