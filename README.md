# Documentation :

	* Squig is a basic interpreted , dynamic toy programming language developed in python v3.10.5 and currently in beta state .
	* Since it's not compiled into an excutable it requires python 3.
	* It's syntax is similar to python.
	
# Limitations:

	* It's slow due to python implementation . But still it can run as fast as python.
	* Everything is global.
	* Squig can'nt handle Errors.
	* Does'nt contains any kind of built-in function.
	* Multiline statements can'nt be used.
	
# Squig datatypes : 
	
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
	
   * We have a new type in squig and that is called InputStringType. 
     It's very similar to StringType , anything that's enclosed within
     a single quotes is considered as InputStringType.
		  
   * As the name suggests it's function is to get the input from the user.
		
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
		

# Print statement : 

    * We can directly print stuffs on the screen.
	
## Syntax  :
	
	{ value }
	
## Example :
	
	Squig > { " Hello world " }
	
    * This displays Hello world on the screen.
    * '{' and '}' are optional as of now.
	

# Variables in Squig : 

    * Variable named by the following rule .
		
		1.) Variable must start with an underscore or letter
		2.) Variable are case sensitive.
		3.) Variable can contain digits.
		
    * The same rule followed in other programming Languages.
	
	
# Assignment statement :

    * Instead of using a equal(=) we use colon(:) for assigning values to variables.
	
## Syntax:
	
	variable : value
	
## Example :
		
	Squig > variable : " Hello world " 
		
     * And it's the only assignment statement available in squig . Shorthan hand operators will be included in the upcoming future.
	
# Input Statement : 

	* To get input from the user we use the InputStringType.
	
## Syntax:
		
		' Message ' --> input statement (or) input string type
	
## Example :
		
		Squig > variable : 'Enter your name : '
		
		Squig > { "Welcome " + variable }
		
# If-elif-else statements :

	* Decision making statement is similar to python if-elif-else but one expection we must added '{','}'
	
## Syntax:
		
		if { condition } : true-block else : false-block
		
		if {condition} : if-block elif {condition} : elif-block else : else-block
	
## Example :
		
		Squig > if { 'Enter a value : ' == 100 } : "True" else : "False"
		
		Squig > name : "Yoen woo jin"

		Squig > if { name == "shinchan" } : "it's a cartoon " elif { name == "Yoen woo jin" } : "Welcome " + name else : "None"
	
# For statement : 

	* Squig supports only one looping statement and that's for loop.
	
## Syntax:
		
		for iter_val{start_value , end_value ,step_value } : for-statement-body
		
	
## Example : 
	
		Squig > for x{10} : {x} --> displays from 0 to 9 on screen
		
		Squig > for x{1,10} : {x} --> displays from 1 to 9 on screen
		
		Squig > for x{1,10,2} : {x} --> displays from 1 to 10 increments the iteration by 2.
		
		
# Function statement : 

	* As like in other programming languages we can declare function in squig using the 'function' keyword.
	* Default arguments are not supported.
	
## Syntax :
	
		function_name function { parameter-1 , parameter-2, ... parameter-n} : function-body
	
## Example :
	
		Squig > patter function {size} : for x{1,size+1} : "* "*x
		Squig > patter{5}
		
## output : 
	
		*
		* *
		* * *
		* * * * 
		* * * * *
		
# Collection statement : 

	* It's similar to pythons list.
	
## Syntax:
			
			[element1,element2,...,element-n]
			
## Example : 
		
			Squig > name : ["shinchan","Doraemon"]
			Squig > {name}
		
		
	* We can access elements from the collecction by using it's index.
	
# Example : 
			
			Squig > name[0]
			
		* Accessing values from nested collection if as follows.
		
			Squig > name : [1,2,[0,9]]
			Squig > name[-1][-1]
			
	* As like other variables we can assign values to the individual collection elements
		
		# Example : 
		
			Squig > name[0]  : "Harish"
			
		* Assigning values to a nested list is not supported as of now.
		
			
			
		
		
		
		
	
			
			
	
