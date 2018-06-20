Installation
------------

with conda:
```
conda create -n componentsDB python=3.6 pymongo mongodb
```

Open **two** terminals and type in both:
```
conda activate componentsDB
```

In one of the two terminals start mongodb indicating a directory where
data should be stored:
```
mongodb --dbpath=$PWD/data
```
Just remove the data directory if you want a clean restart

Testing and running
-------------------
In the other terminal create some components and write them in the
database:
```
python example-write.py
```

To read back the components just created do a:
```
python example-read.py
```

Use the example files as guide. Note that the example include a
user-defined component type, i.e. a class defined in user-code. 

Notes
-----
Code requires a feature of python 3.6, it could be back-ported to older
versions of python with some work (there are notes in the code).

Writing python object to mongoDB is trivial since the dictionary
representation can be stremed directly. Two are the complications: 
the first one is that in our discussions we foreseen components that are 
actually a group of sub-components.
To be more *OO* I have assumed we want the parent object (an instance class) to
own a list of sub-components (other list instances). When writing to a DB
we need to "stream" the objects recursively. The issue is that a
sub-component in principle could belong to more than one parent, thus I
have decided to write in the DB references and avoid embedded data
in MongoDB see
[here](https://docs.mongodb.com/manual/core/data-modeling-introduction/#document-structure)
The second complication is to allow to create an instance of 
a specific class given the name of the class itself (because in the DB there is
written "Quadrupole" as a string and we need to create an object of that
type). Each "component" class inherits from the base class Component and
there is some machinary to "self" register a class type to the system (it
is the reason why we need python 3.6 to do that in a simple way). This
self-registration mechanism allows for user-defined classes to be created
in separate modules and still make them known to the system (see example
files).

Currently objects are uniquely identified by a random UUID, this could be
avoided, because when writing to MongoDB any document written
gets anyway a unique id. However I am not sure how to deal with objects created
by user and not yet written into DB.
Is it possible to get a mongo ID *before* writing it to the DB?
Again on uinique id, the object name could be used as unique id, I did not
do that because I assumed the same name could be used more than once.
Maybe I am wrong here and name is actually unique?

Optimizations: the code is highly inefficient, for example the objects
that are created are stored in a list, so when I need to search by name I
have to loop on all objects, this will be quite slow for large DBs, We
should switch to a dictionary that uses the UUID as a key.
Another alternative could be to completely rely on MongoDB for searching
and querying. Instead of creating pure python objects in memory
representing the components and when needed store/read them in the
database, one could create a MongoDB document every time a new component
object is created. This would allow to have the query power of MongoDB
also for in-memory objects. I like this second approach, but it clearly
makes MongoDB a pre-requisite of running LUME, while in my current
approach it is possible in principle to remove MongoDB entirely and still
run LUME (for example using pickle or json to store the object instances
of components).
