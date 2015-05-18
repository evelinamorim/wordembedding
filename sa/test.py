from document import Document


if __name__ == '__main__':
    doc = Document(textField='reviewComment')
    docList = doc.run('/scratch2/evelin.amorim/WebMD/vectors_webmd.bin',
                      '/scratch2/evelin.amorim/WebMD/test_drugs_reviews.json')
