export ZSH="/home/defoxys/.oh-my-zsh"

ZSH_THEME="robbyrussell"

plugins=(git archlinux pyenv sudo systemd themes docker-compose)

source $ZSH/oh-my-zsh.sh

autoload -Uz compinit
compinit

if [ -z "${DISPLAY}" ] && [ "${XDG_VTNR}" -eq 1 ]; then
  exec startx > /dev/null
fi

alias l='ranger --choosedir=$HOME/.rangerdir; LASTDIR=`cat $HOME/.rangerdir`; cd "$LASTDIR"'
alias v='. venv/bin/activate'
