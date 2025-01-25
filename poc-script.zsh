#!/usr/bin/env zsh

# make fzf see global installation path and not spam my shell startup
# export FZF_PATH="$(which fzf)"

# config for https://github.com/unixorn/fzf-zsh-plugin/tree/main
export FZF_PREVIEW_ADVANCED=true

export FZF_PREVIEW_WINDOW='right:65%:nohidden'

# enable integration with ripgrep-all: https://github.com/phiresky/ripgrep-all/wiki/fzf-Integration

rga-fzf() {
  RG_PREFIX="rga --files-with-matches"
  local file
  file="$(
    FZF_DEFAULT_COMMAND="$RG_PREFIX '$1'" \
      fzf --sort --preview="[[ ! -z {} ]] && rga --pretty --context 5 {q} {}" \
        --phony -q "$1" \
        --bind "change:reload:$RG_PREFIX {q}" \
        --preview-window="70%:wrap"
  )" &&
  echo "opening $file" &&
  xdg-open "$file"
}

# simplify the various fzf file finding aliases to use shared functionality
function fzf-file-helper {
  if (( $# == 0 )); then
  #get selected file with or without input hint
    selectedFile=$(fd -t f . $searchDir | fzf)
  else
    selectedFile=$(fd -t f . $searchDir | fzf  --select-1 --query "$*")
  fi

  if [ -z $selectedFile ]; then
    return
  fi

  # $= forces words to be split so alias works
  $=EDITOR $selectedFile
}

function find-and-edit {
  local searchDir=$1
  shift
  fzf-file-helper $@
}
alias fne="find-and-edit"


# based on https://unix.stackexchange.com/a/566272, quickly cd's into dir
# set up to use history and prefer it to make it more accurate over time
fdcd() {
  local dir
  dir=$(
    cd &&
      fd -0 --type d \
        --ignore-file ~/.config/fd/ignore |
      fzf --read0 --history="$HOME/.config/fzf/history" --scheme=history
  ) && cd ~/$dir || return
  if zle; then
    # allow fdcd to run inside and outside zle
    zle reset-prompt
  fi
}

get-destination() {
  local dir

  # make directory for fzf history if need be, otherwise does nothing
  mkdir -p "$HOME/.config/fzf"

  # continuously poll for directories until destination is chosen
  while [[ -z $dir ]]; do
  dir=$(
    cd &&
    fd -0 --type d \
      --ignore-file ~/.config/fd/ds_ignore --follow | # follow symlinks
    sed 's/\.\///g' | # trim off leading ./ from each result
    sed 's/$/\0Trash/' | # add entry for trash folder at end
    fzf --read0 --history="$HOME/.config/fzf/dest_history" --scheme=history

  )
  done

  echo $dir
}

# master download-sorting command
ds() {
  # create local variables
  local choice
  local destination_confirmed

  # check if dir not empty, from chatgpt
  while ! [[ -z "$(eza $HOME/Downloads)" ]]; do
    # use fzf on downloads folder to get list of items to move to first folder
    ############################################################################
    # change line selector to turn fzf output list into zsh array
    local origIFS=$IFS
    IFS=$'\n'

    # surrounding parentheses turn batch into a zsh array: https://gist.github.com/ClementNerma/1dd94cb0f1884b9c20d1ba0037bdcde2#arrays
    # important to not have eza output quotes or breaks filenames with spaces
      local batch=($(eza --sort=modified --reverse --no-quotes ~/Downloads |
                       fzf --multi --exit-0 --no-sort \
                         --prompt "Choose files: "))

    # reset IFS back to original value
    IFS=$origIFS
    ########################################################################
    # use fzf with filters to interactively select destination dir
    ########################################################################
    local dir=$(get-destination)
    ########################################################################
    # feed selected files into interactive mv command
    ########################################################################
    destination_confirmed=false

    while ! $destination_confirmed; do
      echo "chosen files are: ${batch[@]}"
      echo "destination is: $dir"

      # q flag outputs n otherwise, so just read regularly
      read "choice?Continue with move? [Y/n] " # https://stackoverflow.com/a/15174634

      # if empty or y/Y, proceed
      if [[ "$choice" =~ "^[Yy]$|^$" ]]; then # string match from chatgpt
        cd ~/Downloads

        # use trash program if trash is selected destination
        if [[ "$dir" == "Trash" ]]; then
        # loop over values in case of names with spaces
          for file in $batch; do
            trash "$file" && #filename already quoted, so no need to add extra
          done
          echo "Files moved to trash."

        else
          # move without overwriting into dest
          # do for each array element individually in case there are spaces in the name
          for file in $batch; do
            mv --interactive --verbose "$file" "$HOME/$dir" &&
          done
          echo "Move complete!"

        fi

        # set destination selection so loop ends
        destination_confirmed=true
      else
        read "choice?Move canceled. Change destination? [Y/n]"

        if [[ "$choice" =~ "^[Yy]$|^$" ]]; then
          echo
          dir=$(get-destination)
        else
          echo "Exiting sorter."
          return
        fi
      fi
      done

    echo
  done

  echo "Downloads folder cleared!"
  return
}
