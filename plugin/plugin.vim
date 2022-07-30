if !has("python3")
    echo "vim has to be compiled with +python3 to run this"
    finish
endif


if exists('g:auto_summary_loaded')
    finish
endif


" Returns the directory of the first file in `argv` or `cwd` if it's empty
function FindSessionDirectory() abort
    if len(argv()) > 0
        return fnamemodify(argv()[0], ':p:h')
    endif
    return getcwd()
endfunction!
let g:session_default_directory = FindSessionDirectory()


let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')
py3 << EOF
import sys
import vim
from pathlib import Path


plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = Path(str(plugin_root_dir)) / '..' / 'auto_summary'
sys.path.insert(0, str(python_root_dir.resolve()))
import generate_summary
EOF


function! Summarize(...)
    if a:0 > 0
        let root = a:1
    else
        let root = 0
    endif
py3 << EOF
root = vim.eval('root')
# debug purpose
# vim.command('echom root')

if root != "0":
    # if path is specified, run summarizer there
    root = Path(root).resolve()
    if not root.exists():
        vim.command('echomsg "PATH DOES NOT EXIST!"')
    else:
        vim.command(f'let g:auto_summary_root="{str(root)}"')
        generate_summary.main(root)
else:
    # else run summarizer, where current vim session started
    session_default_directory = Path(vim.eval('g:session_default_directory')).resolve()
    vim.command(f'let g:auto_summary_root="{str(session_default_directory)}"')
    generate_summary.main(session_default_directory)
EOF
endfunction
command! -nargs=* Summarize call Summarize(<f-args>)
