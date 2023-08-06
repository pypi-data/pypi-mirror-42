# EVE
A lightweight data-interchange format.


# Example use
example.eve
```
[
  @ This is a comment
  
  @ String variables
  'Name' :: 'Eric'
  'Age' :: '21'
  'Country' :: 'USA'
  'City' :: 'New York'
  
  @ Boolean variables
  ?hasGirlfriend = False
];
```

example.py
```python
import eve

result = eve.load('example.eve')
print(result['Name']) # And so on
result['Age'] = '22'
eve.save(result, 'example.eve')
```


# ATOM grammar syntax highlighting
1. Copy the folder: `eve` in the `editors\atom` folder
2. Paste that to the `.atom` folder in `C:\Users\yourusername\.atom\packages`
3. Now restart ATOM and it should work
