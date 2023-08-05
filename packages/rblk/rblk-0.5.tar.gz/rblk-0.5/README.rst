======
rblk
======
- recursive match nested brackets  


Installation
------------
    ::
    
    $ pip3 install rblk


License
-------

- MIT


Examples
--------

- *code-string*

    ::
        
        from rblk.txt import Parser
        
        txt = '''(defun last-state (rewindable)\
        (let((size (rewind-count rewindable)))\
        (if(zerop size)(values nil nil)\
        (values (aref (rewind-store rewindable) (1- size)) t))))'''
        
        tag_pairs = '()'
        
        p = Parser(txt,tag_pairs)
        dummy = [print(each) for each in p.srch4txt()]
        dummy = [print(each) for each in p.text_mat]
        
.. image:: ./docs/images/lisp.0.png
.. image:: ./docs/images/lisp.1.png


- *self-defined-structure*

    ::
        
        from rblk.txt import Parser
        txt = '''<0x1x2x<3x4>x[5x6x{{{7}}}]x@9#10#@>'''
        
        tag_pairs = '<>[]{}@@##'
        
        p = Parser(txt,tag_pairs)
        dummy = [print(each) for each in p.text_mat]
        dummy = [print(each) for each in p.srch4txt()]
        

.. image:: ./docs/images/self_defined_struc.0.png


Quickstart
----------


        

- *init Parser with tag_pairs*
    
    ::
    
        from rblk.txt import Parser
        txt = '''SSS{ABC"UVW(axb)"MMM[aa]vv(bb(c()c))}<rr<ss>tt>UUU'''
        tag_pairs = '""{}()[]<>'
        p = Parser(txt,tag_pairs)
        
   
- *text_mat*

    ::
        
        dummy = [print(each) for each in p.text_mat]
        
        >>> dummy = [print(each) for each in p.text_mat]
        ['SSS{ABC"UVW(axb)"MMM[aa]vv(bb(c()c))}<rr<ss>tt>UUU']
        ['SSS', '{ABC"UVW(axb)"MMM[aa]vv(bb(c()c))}', '<rr<ss>tt>', 'UUU']
        ['ABC', '"UVW(axb)"', 'MMM', '[aa]', 'vv', '(bb(c()c))', 'rr', '<ss>', 'tt']
        ['UVW', '(axb)', 'aa', 'bb', '(c()c)', 'ss']
        ['axb', 'c', '()', 'c']
        >>>

- *srch4blk*

    ::

        p.srch4blk('(') 

        >>> p.srch4blk('(')
        ['(bb(c()c))', '(axb)', '(c()c)', '()']
        >>>

        p.lvsrch4blk('(',3)

        >>> p.lvsrch4blk('(',3)
        ['(axb)', '(c()c)']
        >>>



- *srch4txt*
  
  ::
      
        p.srch4txt()
        
        >>> p.srch4txt()
        ['SSS', 'UUU', 'ABC', 'MMM', 'vv', 'rr', 'tt', 'UVW', 'aa', 'bb', 'ss', 'axb', 'c', 'c']
        >>>


- *lvsrch4txt*

    ::

        p.lvsrch4txt(2)

        >>> p.lvsrch4txt(2)
        ['ABC', 'MMM', 'vv', 'rr', 'tt']
        >>>


- *lvsrch4txt_fromto*

    ::

        p.lvsrch4txt_fromto(2,3)
        >>> p.lvsrch4txt_fromto(2,3)
        ['ABC', 'MMM', 'vv', 'rr', 'tt']
        >>>

     
- *self-defined tag_pairs*

    ::

        >>> txt = '''{ddd@#ddd>'''
        >>> tag_pairs = '{@#>'
        >>> p = Parser(txt,tag_pairs)
        >>> dummy = [print(each) for each in p.text_mat]
        ['{ddd@#ddd>']
        ['{ddd@', '#ddd>']
        ['ddd', 'ddd']
        >>>

- *chinese-tag_pairs*

    ::

        from rblk.txt import Parser
        txt = '''的dd的【人【uu】人】'''
        tag_pairs = '的的【】'
        p = Parser(txt,tag_pairs)
        dummy = [print(each) for each in p.text_mat]
        
        p.srch4txt()


        >>> dummy = [print(each) for each in p.text_mat]
        ['的dd的【人【uu】人】']
        ['的dd的', '【人【uu】人】']
        ['dd', '人', '【uu】', '人']
        ['uu']
        >>>
        >>> p.srch4txt()
        ['dd', '人', '人', 'uu']
        >>>



Usage and APIs
--------------

- refer to `Usage <./docs/Usage.rst>`_
        

Features
--------

- self define brackets
- nested match


Restrict
--------

- 

TODO
----

- array parser 
- complicated tag support(such as html)


References
----------

* elist
* edict
