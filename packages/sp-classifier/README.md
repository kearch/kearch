# Specialist Classifer
## Classify a webpage using body words and title words
Comment: Use POST query because parameters may be too long for GET query.
Access URL (POST)
```
$(ip adress of the specialist classifier)/sp/classifier/classify
```
JSON to POST  
```
{
    'data':{
        'body_words': ['haskell', 'lisp'],
        'title_words': ['julia']
    }
}
```
Result  
Comment: Result is kearch_classifier.classifier.IN_TOPIC or kearch_classifier.classifier.OUT_OF__TOPIC
```
{
    'result': 1
}

