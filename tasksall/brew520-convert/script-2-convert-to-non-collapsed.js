const fs = require('fs');
const { keywords } = require('./constants');

function replacePrefixForAllKeysInObject(obj){
    Object.keys(obj).forEach(key => {
        obj[`offers.${key}`] = obj[key];
        delete obj[key];
    });
}

function replacePrefixForAllKeysInArray(array){
    for(let i=0; i<array.length; i++) {
        array[i] = `offers.${array[i]}`
    }
}

async function main(){
    keywords.forEach(function(keyword){
      console.log(`converting: ${keyword}`)
        let json = JSON.parse(fs.readFileSync(`./original/${keyword}.json`));
        const query = json.body[1];
        delete query['collapse'];
        query['_source'] = { excludes: ["offers"]}
        query['query'] = {
            "nested": {
                "path": "offers",
                "query": query['query'],
                "inner_hits": {}
            }
        }
        const functionalBoolQuery = query['query']['nested']['query']['function_score']['query']['bool'];
        
        ["must", "should", "must_not", "filter"].forEach(type => {
          const queries = functionalBoolQuery[type];
          if(!queries){
            return ;
          }
          for(let i=0; i<queries.length; i++){
            const typeQuery = queries[i];
            if(typeQuery['multi_match']){
              replacePrefixForAllKeysInArray(typeQuery["multi_match"]["fields"]);
            }
            if(typeQuery['range']){
              replacePrefixForAllKeysInObject(typeQuery['range']);
            }
            if(typeQuery['match']){
              replacePrefixForAllKeysInObject(typeQuery['match']);
            }
            if(typeQuery['term']){
              replacePrefixForAllKeysInObject(typeQuery['term']);
            }
            if(typeQuery['terms']){
              replacePrefixForAllKeysInObject(typeQuery['terms']);
            }
          }
        });
        const functions = query['query']['nested']['query']['function_score']['functions'];
        for(let i=0; i<functions.length; i++){
          const f = functions[i];
          if(f['field_value_factor'] && f['field_value_factor']['field'] == 'staticScore'){
            f['field_value_factor']['field'] = 'offers.staticSore';
          }
          if(f['script_score'] && f['script_score']['script'] && f['script_score']['script']['source']){
            f['script_score']['script']['source'] = f['script_score']['script']['source'].replace(/doc\[\"(\w+)\"\]/g, `doc["offers.$1"]`)
          }
          if(f['filter'] && f['filter']['bool'] && f['filter']['bool']['should']){
            const arr = f['filter']['bool']['should'];
            for(let j=0; j<arr.length; j++){
              if( arr[j]['multi_match']){
                replacePrefixForAllKeysInArray(arr[j]['multi_match']['fields'])
              }
            }
          }
        }

        query['aggs'] = {
          "filters": {
            "nested": {
              "path": "offers"
            },
            "aggs": {
              "brands": {
                "terms": { "field": "offers.brandId", "size": 500 }
              },
              "categories": {
                "terms": { "field": "offers.categoryLv3Id", "size": 500 }
              },
              "stores": {
                "terms": { "field": "offers.orcaMerchantId", "size": 500 }
              }
            }
          }
        }
        fs.writeFileSync(`./non-collapsed/${keyword}.json`, JSON.stringify(query));
    })
}

main();
