#!/bin/bash
# ----------------------------------------------------------------------------------------------------------------------
# OBITEC Django Installer
# ----------------------------------------------------------------------------------------------------------------------
# Setup and create a new Django project based on OBITECS' djskel template.


# LICENSE
# ----------------------------------------------------------------------------------------------------------------------
# Copyright (c) 2014 OBITEC Consultig (Pty) Ltd
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# SETTINGS
# ----------------------------------------------------------------------------------------------------------------------
# Max number of arguments, empty value = unlimited arguments
SCRIPT_MAX_ARGS=1


# INITIALIZE
# ----------------------------------------------------------------------------------------------------------------------
SCRIPT_NAME="$(basename "$0")"
# Stores arguments
SCRIPT_ARGS=()
# Stores option flags
kwargs=()
# For returning value after calling get_kwarg
kwarg_value=

#Alternative colour settings
t_normal=$(tput sgr0)
t_bold=$(tput bold)
f_red=$(tput setaf 1)
f_green=$(tput setaf 2)
f_yellow=$(tput setaf 3)
f_blue=$(tput setaf 4)
f_magenta=$(tput setaf 5)
f_cyan=$(tput setaf 6)


# BOILERPLATE FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------
# Usage for -h|--help
usage () {
  echo "Usage: $SCRIPT_NAME [options] [arguments]

OPTIONS:
    --no-color   do not use colors
    -h, --help   display this help and exit

EXAMPLES:
    $SCRIPT_NAME demo_project --app=demo_app --python=/usr/bin/python
"
}

# Usage: info "message"
# Example: info "It's Working"
# Output (to STDOUT): [...] It's Working
info (){
    printf "%b" "[${f_green}...${t_normal}] $1\n"
}

# Usage: prompt "question"
# Example: prompt "What's Your Name?"
# Output (to STDOUT): [ ? ] What's Your Name?  
prompt (){
    printf "%b" "[${f_yellow} ? ${t_normal}] $1 "
}

# Usage: error ["message"]
# Example: error "You're Ugly"
# Output (to STDERR): [ERROR] /script/name: You're Ugly
error (){
    printf "%b" "[${f_red}ERROR${t_normal}] ${0}: ${1:-'Unkown Error'}\n" >&2
}

# Usage: fail "message" [exit_code]
# Example: fail "Unknown Option" 254
fail (){
    error "$1"

    case $2 in
        ''|*[!0-9]*)
            exit_code=1
            ;;
        *)
            exit_code=$2
        ;;
    esac
    
    echo -e ${f_red}
    echo -e "Try \`$SCRIPT_NAME --help' for more information." >&2
    echo -e ${t_normal}
    exit ${exit_code}
}

# ask function https://gist.github.com/davejamesmiller/1965569
# Usage: ask "Yes or No?" [default option]
# Example: if "Yes or No?" Y; then
ask (){
    while true; do
 
        if [ "${2:-}" = "Y" ]; then
            prompt_tail="Y/n"
            default=Y
        elif [ "${2:-}" = "N" ]; then
            prompt_tail="y/N"
            default=N
        else
            prompt_tail="y/n"
            default=
        fi
 
        # Ask the question
        prompt "$1 [$prompt_tail]"
        read REPLY
 
        # Default?
        if [ -z "$REPLY" ]; then
            REPLY=$default
        fi
 
        # Check if the reply is valid
        case "$REPLY" in
            Y*|y*) return 0 ;;
            N*|n*) return 1 ;;
        esac

    done
}

argument_expected(){
    fail "$1 expected an argument"
}

finally(){
    if [ ! -z $example_one ]; then
        info "Finally, Example One: \"$example_one\""
    fi

    if [ ! -z $example_two ]; then
        info "Finally, Example Two: \"$example_two\""
    fi

}

parse_options() {
  while (( $#>0 )); do
    opt="$1"
    arg="$2"
    
    case "$opt" in
      -p|--python-path)
          #if echo "$opt" | grep -q "="; then
          #    python_path="$(echo "$opt" | cut -f2 -d=)"
          #else
          #    #i=$(( $i + 1 ))
          #    python_path="$arg"
          #fi;
        set_kwarg "python_path" "$arg" 1
        shift
        ;;
      -n|--project-name)
        set_kwarg "project_name" "$arg" 1
        shift
        ;;
      -a|--app-name)
        set_kwarg "app_name" "$arg" 1
        shift
        ;;
      --no-color)
        set_kwarg "no_color"
        shift
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      -*)
        fail "$SCRIPT_NAME: invalid option -- '$opt'"
        ;;
      *)
        if [[ ! -z ${SCRIPT_MAX_ARGS} ]] && (( ${#SCRIPT_ARGS[@]} == ${SCRIPT_MAX_ARGS} )); then
          fail "$SCRIPT_NAME: cannot accept any more arguments -- '$opt'" 1
        else
          SCRIPT_ARGS=("${SCRIPT_ARGS[@]}" "$opt")
        fi
        ;;
    esac
    shift
  done
}

# SCRIPT TEMPLATE FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------
# Stores options
# $1 - option name
# $2 - option value
# $3 - non-empty if value is not optional
set_kwarg () {
  if [[ ! -z "$3" ]] && [[ -z "$2" ]]; then
    fail "$SCRIPT_NAME: missing option value -- '$opt'" 1
  fi
  # XXX should check duplication, but doesn't really matter
  kwargs=("${kwargs[@]}" "$1" "$2")
}

# Checks if an option is set, also set kwarg_value.
# Returns 0 if found, 1 otherwise.
get_kwarg () {
  local i opt needle="$1"
  for (( i=0; i<${#kwargs[@]}; i+=2 )); do
    opt="${kwargs[i]}"
    if [[ "$opt" == "$needle" ]]; then
      kwarg_value="${kwargs[i+1]}"
      #echo "${needle} = ${kwarg_value}"
      return 0
    fi
  done
  #echo "not found ${needle}"
  kwarg_value=
  return 1
}

set_color_variables () {
  local COLORS=(black red green yellow blue magenta cyan white)
  local i SGRS=(normal bold ___ italic ___ black ___ invert)
  for (( i=0; i<8; i++ )); do
    eval "f_${COLORS[i]}=\"\e[3${i}m\""
    eval "b_${COLORS[i]}=\"\e[4${i}m\""
    eval   "t_${SGRS[i]}=\"\e[${i}m\""
  done
}



# FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------
check_python(){

    if [ "$python_path" = "" ]; then
        if get_kwarg "python_path"; then
            python_path=${kwarg_value}
        else
            python_path="$(command \which python3)"
        fi
    fi
    #python_path=$(type ${kwarg_value} | grep -Po '( /.+)$')

    info "Python: ${python_path}"

    if [ ! -z "${python_path}" ]; then
        info "Using python path: '${python_path}'"
    else
        error "Python3 not found"
        ask "Do you want to install it?" "Y"
    fi
    
}

init_virtualenvwrapper(){
    VIRTUALENVWRAPPER="$(command \which virtualenvwrapper.sh)"
    if [ "$VIRTUALENVWRAPPER" = "" ]; then
        ask "Install virtualenv wrapper?" "Y"
    fi

    export PROJECT_HOME=/home/canary/Projects
    export WORKON_HOME=/home/canary/Virtualenvs
    export VIRTUALENVWRAPPER_PYTHON=${python_path}
    source $VIRTUALENVWRAPPER
}


delete_project(){
    get_kwarg "project_name"; project_name=${kwarg_value}
    if [ -z ${project_name} ]; then fail "Please specify project name"; fi
    info "Deleting project '${project_name}'..."

    init_virtualenvwrapper

    rmvirtualenv ${project_name}
    rm -Rf ${PROJECT_HOME}/${project_name}/ 
}

create_project(){
    get_kwarg "project_name"; project_name=${kwarg_value}
    if [ -z ${project_name} ]; then fail "Please specify project name"; fi

    info "Creating project '${project_name}'..."

    init_virtualenvwrapper

    if ! mkproject --system-site-packages --python=${python_path}  ${project_name}; then
        workon ${project_name}
    fi

    if [ ! -d ".skel" ]; then
        git clone ssh://ocean_git/~/djskel .skel
        info "Cloned .skel folder"
    else
        cd .skel
        git pull
        cd ../
        info "Updated .skel folder"
    fi

    pip3 install django

    django-admin startproject \
        --template=.skel/project_template \
        --extension=py --extension=conf --extension=sh --extension=ini \
        ${project_name}

    mv ${project_name}/* ./
    mv ${project_name}/.gitignore ./
    rm -R ${project_name}

    chmod +x src/manage.py

    #pip install -U -r var/requirements/development.txt
    pip install -r var/requirements/development.txt

    mkdir -p tmp var/log var/www/media/uploads

    touch \
      src/config/apps-enabled.txt \
      var/log/django.log \
      var/log/nginx-error.log \
      var/log/nginx-access.log

    ./src/manage.py syncdb

    ./src/manage.py createsuperuser

    #Check if app name is specified as well
    get_kwarg "app_name"; app_name=${kwarg_value}
    if [ ! -z ${app_name} ]; then create_app; fi

    git init
    git add -A
    git commit -a -m "Skeleton app added from djskel"

    ssh -t ocean_ssh "sudo /srv/data/git/git-shell-commands/create ${project_name}"
    
    git remote add origin ssh://ocean_git/~/${project_name}
    git push --set-upstream origin master

    chown canary:webapps tmp/uwsgi.sock

}

create_app(){
    #Get project name
    get_kwarg "project_name"; project_name=${kwarg_value}
    if [ -z ${project_name} ]; then fail "Please specify project name"; fi
    
    #Get app name
    get_kwarg "app_name"; app_name=${kwarg_value}
    if [ -z ${app_name} ]; then fail "Please specify app name"; fi

    #Init virtualenvwrapper and test if project exists
    init_virtualenvwrapper
    if ! workon ${project_name}; then fail "First create project!"; fi

    if grep ${app_name} src/config/apps-enabled.txt; then
        fail "App name already registered" 1
    fi

    info "Adding app to project '${project_name}'..."
    ./src/manage.py startapp --template=.skel/app_template --extension=py ${app_name}
    mv ${app_name} src/
    echo ${app_name} >> src/config/apps-enabled.txt
    ./src/manage.py makemigrations ${app_name}
    ./src/manage.py migrate ${app_name}

}

# MAIN
# ----------------------------------------------------------------------------------------------------------------------
main(){
    if [ -z $1 ]; then
        usage
        exit 0        
        #fail "You must specify at least a project name"
    fi

    parse_options "$@"

    if ! get_kwarg "no_color"; then
      set_color_variables
    fi

    check_python
    script_command=${SCRIPT_ARGS[0]}


    case "${script_command}" in
      create)
        create_project
        ;;
      delete)
        delete_project
        ;;
      create_app)
        create_app
        ;;
      *)
        fail "Unrecognised command" 1
        ;;
    esac

}

main "$@"
