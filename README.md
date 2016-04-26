# Dredd
                          ______
                       ,-~   _  ^^~-.,
                     ,^        -,____ ^,         ,/\/\/\,
                    /           (____)  |      S~        ~7
                   ;  .---._    | | || _|     S  I AM THE  Z
                   | |      ~-.,\ | |!/ |     /_   LAW!   _\ 
                   ( |    ~<-.,_^\|_7^ ,|     _//_      _\
                   | |      ", 77>   (T/|   _/'   \/\/\/
                   |  \_      )/<,/^\)i(|
                   (    ^~-,  |________||
                   ^!,_    / /, ,'^~^',!!_,..---.
                    \_ "-./ /   (-~^~-))' =,__,..>-,
                      ^-,__/#w,_  '^' /~-,_/^\      )
                   /\  ( <_    ^~~--T^ ~=, \  \_,-=~^\
      .-==,    _,=^_,.-"_  ^~*.(_  /_)    \ \,=\      )
     /-~;  \,-~ .-~  _,/ \    ___[8]_      \ T_),--~^^)
       _/   \,,..==~^_,.=,\   _.-~O   ~     \_\_\_,.-=}
     ,{       _,.-<~^\  \ \\      ()  .=~^^~=. \_\_,./
    ,{ ^T^ _ /  \  \  \  \ \)    [|   \oDREDD >
      ^T~ ^ { \  \ _\.-|=-T~\\    () ()\<||>,' )
       +     \ |=~T  !       Y    [|()  \ ,'  / -naughty


Dredd is a law enforcement officer in the dystopian future city of Amazon Web Services. He is a street judge, empowered to summarily arrest, convict, sentence, and terminate EC2 unhealthy instances.

## Motivation
Amazon Auto Scaling Groups automatically replace instances marked as unhealthy from your cluster with fresh and new healthy instances, but it only allow you to define healthchecks based on EC2 healthcheck or ELB healtcheck.
The problem with EC2 healthcheck is that the instance could be running fine, but the service inside stopped for whatever reason. In that case, the Auto Scaling Group will never notice it, so it'll never replace this unhealthy instance.

You can solve this with ELB healthchecks, but you have to pay for each ELB.
