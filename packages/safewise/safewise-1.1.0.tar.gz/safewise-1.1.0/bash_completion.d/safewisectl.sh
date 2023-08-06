_safewisectl()
{
    export SafeWISECTL_COMPLETION_CACHE
    local cur prev cmds base

    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    if [ -z "$SafeWISECTL_COMPLETION_CACHE" ]; then
        help_output=$(safewisectl --help | grep '^  [a-z]' | awk '{ print $1 }')
        export SafeWISECTL_COMPLETION_CACHE="$help_output"
    fi

    cmds="$SafeWISECTL_COMPLETION_CACHE"

    COMPREPLY=($(compgen -W "${cmds}" -- ${cur}))
    return 0
}

complete -F _safewisectl safewisectl
