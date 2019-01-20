# NLPwithSpacy
Currently, we are using Hierarchical rules with regular expression. 
In future, we are concentrating to train the model for the same.
### PipeLine as follows:
  * Tokenization with spacy
  * Post processing the tokens.
  * German named entity recognizer with custom-classes(user-defined).
    - For German NER we are using spacy phraseMatcher and Matcher.
  * Parts-of-speech tagging with NLTK library.
    - nltk.stanford has pos tagging model.
  * Detecting roman numerals.
    #### Some custom Rules   
  * ### followed by 
  * Dbpedia reolution
  * Munpex German Chunker
  * DBpedia_NP_filter
