from item import Item

import requests

variables = {
    "categoryId": None,
    "storeIds": None,
    "pagingInfo": {"offset":0,"limit":999999},
    "pageSlug": "actions",
    "random": True
    }

query = '''
query offers($categoryId: ID, $storeIds: [ID], $pagingInfo: InputBatch!, $pageSlug: String!, $random: Boolean!) {
  offersSplited(categoryId: $categoryId, storeIds: $storeIds, pagingInfo: $pagingInfo, pageSlug: $pageSlug, random: $random) {
    products {
      count
      items {
        ... on Product {
          ...OptimizedProductsFragment
        }
      }
    }
  }
}

fragment OptimizedProductsFragment on Product {
  id
  slug
  type
  title
  category {
      id
      title
  }
  weight
  imageUrl
  articul
  price
  oldPrice
}
'''

base_url = 'https://silpo.ua/offers/lol/'

def parse():
    response = requests.post('https://silpo.ua/graphql', json={'query': query, 'variables': variables}).json()

    items = []

    for item in response['data']['offersSplited']['products']['items']:

        items.append(Item('silpo', item['title'], item['price'], item['oldPrice'], base_url + item['slug'], item['imageUrl'], item['category']['id'], None))

    return items