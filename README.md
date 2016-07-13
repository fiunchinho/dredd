# Dredd
[![Build Status](https://travis-ci.org/fiunchinho/dredd.svg?branch=master)](https://travis-ci.org/fiunchinho/dredd)
[![Coverage Status](https://coveralls.io/repos/github/fiunchinho/dredd/badge.svg?branch=master)](https://coveralls.io/github/fiunchinho/dredd?branch=master)

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


Dredd is a law enforcement officer in the dystopian future city of *Amazon Web Services*. He is a street judge, empowered to summarily arrest, convict, sentence, and terminate EC2 unhealthy instances.

## Motivation
Amazon Auto Scaling Groups automatically replace instances marked as unhealthy from your cluster with fresh and new healthy instances, but it only allows you to define health checks based on EC2 the health check or the ELB health check.
The problem with the EC2 health check is that the instance could be running fine, but the service inside has stopped for whatever reason. In that case, the Auto Scaling Group will never notice it, so it'll never replace this unhealthy instance.

You can solve this with ELB health checks, but you have to pay for each ELB.

## Installation
You can install this module using pip

```bash
pip install git+https://github.com/fiunchinho/dredd.git
```

## Usage

```bash
$ dredd -u eureka -e "http://your-eureka-host.com:8080/eureka-server/v2/apps"
```

## Tests
You can run the unit tests using tox

```bash
$ tox
```