# SQUIG PROGRAMMING LANGUAGE v0.0.1

## Documentation :

  * Squig is a basic interpreted , dynamic programming language developed in python v3.10.5 and currently in beta state.
  * It's syntax is similar to python.
  
### Note : Squig is not ready for use.

## Goal of Squig:

   * User should able to control the hardware of the computer in a simple way.
   
## Challenge :

  * Since python is used in the back end it will be more difficult to get the control of the hardware system. 
  
  
## Current Limitations :

   * Everything is global.
   * Can not assign values to nested collections.
   * Squig can'nt handle Errors.
   * No built-in function.
   * Multiline statements can'nt be used.
	
## Squig datatypes : 
	
   * NumberType 
   * StringType
   * InputStringType
   * CollectionType
   * BoolType

## NumberType :
		
   * All real number are valid in squig and represented as NumberType.
		

## StringType :
		
   * As like in other programming languages anything that's enclosed 
     within double quotes is considered as StringType.
     
   * We don't have CharacterType in Squig.
		
## InputStringType : 
	
   * Squig has a new datatype called InputStringType. 
     It's very similar to StringType.
		  
   * As the name suggests it is the input statement in squig.
   
   * Anything enclosed with in singel quotes are called InputStringType.
		
### Example :
		
	name : 'Enter your name : '
			
	{ "Welcome " + name }
			
### Output : 
			
	Enter your name : Shinchan
	Welcome Shinchan
		
		
## CollectionType :
		
  * CollectionType is same as python's list.
		
## BoolType :
	
  * BoolType represents 'true' or 'false'
		

## Print statement : 

  * We can directly print stuffs on the screen just by enclosing the value with '{' and '}'.
	
## Syntax  :
	
	{ value }
	
## Example :
	
	{ " Hello world " }
	
  * This displays Hello world on the screen.
  * '{' and '}' are optional as of now.
	

## Variables in Squig : 

  * Variable named by the following rule .
		
    1.) Variable must start with an underscore or letter
    
    2.) Variable are case sensitive.
    
    3.) Variable can contain digits.
		
  * The same rule followed in other programming Languages.
	
	
## Assignment statement :

  * Instead of using a equal(=) we use colon(:) for assigning values to variables.
	
## Syntax:
	
	variable : value
	
## Example :
		
        variable : " Hello world " 
		
   * And it's the only assignment statement available in squig . Shorthan hand operators will be included in the upcoming future.
	
## Input Statement : 

   * To get input from the user we use the InputStringType.
	
## Syntax:
		
	' Message ' --> input statement (or) input string type
	
## Example :
		
	variable : 'Enter your name : '
		
	{ "Welcome " + variable }
		
## If-elif-else statements :

  * Decision making statement is similar to python if-elif-else but one expection we must added '{','}'
	
## Syntax:
		
	if { condition } : true-block else : false-block
		
	if {condition} : if-block elif {condition} : elif-block else : else-block
	
## Example :

        name : "Yoen woo jin"
		
	if { 'Enter a name : ' == name } : "True" else : "False"
	
## For statement : 

  * Squig supports only one looping statement and that's for loop.
	
## Syntax:
		
	for iter_val{start_value , end_value ,step_value } : for-statement-body
		
	
## Example : 
	
	for x{10} : {x} --> displays from 0 to 9 on screen
		
	for x{1,10} : {x} --> displays from 1 to 9 on screen
		
	for x{1,10,2} : {x} --> displays from 1 to 10 increments the iteration by 2.
		
		
## Function statement : 

  * As like in other programming languages we can declare function in squig using the 'function' keyword.
  * Default arguments are not supported.
	
## Syntax :
	
	function_name function { parameter-1 , parameter-2, ... parameter-n} : function-body
	
## Example :
	
	pattern function {size} : for x{1,size+1} : "* "*x
	pattern{5}
		
## output : 
	
	*
	* *
	* * *
	* * * * 
	* * * * *
		
## Collection statement : 

   * It's similar to pythons list.
	
## Syntax:
			
	[element1,element2,...,element-n]
			
## Example : 
		
	name : ["shinchan","Doraemon"]
	{name}
		
		
  * We can access elements from the collecction by using it's index.
	
## Example : 
			
	name[0]
			
  * Accessing values from nested collection if as follows.
		
	name : [1,2,[0,9]]
	name[-1][-1]
			
  * As like other variables we can assign values to the individual collection elements
		
## Example : 
		
	name[0]  : "Harish"
			
* Assigning values to a nested list is not supported as of now.
		
