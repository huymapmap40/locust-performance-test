Offer = '''
{
  id
  title
  offerTypeName
  price
  ageLimit
  ctime
  startTime
  endTime
  status
  tag
  boostTag
  promoteTag
  imageUrl
  merchantIds
  segmentQueryId
  segmentQueryName
  offerGroupId
  offerGroupName
  offerCashback {
    amountFloat
    regularAmountFloat
    sign
    description
    modifier
  }
  merchantCashbacks {
    amountFloat
    regularAmountFloat
    sign
    description
    modifier
    merchantId
  }
  opportunityId
  totalRedeemableCount
  offerUse
  partnerName
  adsTag
  products {
    id
    imageUrl
    title
    price
    subcategory {
      names
    }
    brand {
      name
    }
  }
  campaigns {
    id
    title
    url
  }
}
'''

Offers = f'''
{{
  total
  offers {Offer}
  indexName
}}
'''

Merchants = '''
{
  merchants {
    id
    name
    shortName
    description
    tag
    imageUrl
    limitation
    shortLimitation
  }
}
'''

Campaign = '''
{
  id
  title
  description
  startTime
  endTime
  imageUrl
  rules
}
'''

Category = '''
{
  id
  name
  parentId
  order
  ageLimit
  imageId
  names
}
'''