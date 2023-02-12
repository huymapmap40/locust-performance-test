const fs = require('fs');
const { keywords } = require('./constants');

async function main(){
    keywords.forEach(function(keyword){
      console.log(`converting: ${keyword}`)
        let json = JSON.parse(fs.readFileSync(`./original/${keyword}.json`));
        delete json.body[1]['collapse']
        fs.writeFileSync(`./original-remove-collapse/${keyword}.json`, JSON.stringify(json));
    })
}

main();
