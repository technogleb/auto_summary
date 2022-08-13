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

let g:watch_markdown_changes = get(g:, 'watch_markdown_changes', '0')

py3 << EOF
import sys
import vim
from pathlib import Path

plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = Path(str(plugin_root_dir)) / '..'
sys.path.append(str(python_root_dir.resolve()))
from auto_summary import generate_summary

watch_markdown_changes = vim.eval('g:watch_markdown_changes')
if watch_markdown_changes == '1':
    # check if watchdog is installed
    try:
        import watchdog
        from auto_summary import change_watcher
    except ImportError:
        vim.command(
            'echoerr "You do not have watchdog installed. Please install it using ' \
            'the python your vim was compiled with by `python -m pip install watchdog.`' \
            'If you are using neovim, install with your currently used python."'
        )
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

watch_markdown_changes = vim.eval('g:watch_markdown_changes')
if root != "0":
    # if path is specified, run summarizer there
    root = Path(root).resolve()
    if not root.exists():
        vim.command('echomsg "PATH DOES NOT EXIST!"')
    else:
        vim.command(f'let g:auto_summary_root="{str(root)}"')
        if watch_markdown_changes == '1':
            change_watcher.watch(root)
        else:
            generate_summary.main(root)
else:
    # else run summarizer, where current vim session started
    session_default_directory = Path(vim.eval('g:session_default_directory')).resolve()
    vim.command(f'let g:auto_summary_root="{str(session_default_directory)}"')
    if watch_markdown_changes == '1':
        change_watcher.watch(session_default_directory)
    else:
        generate_summary.main(session_default_directory)
EOF
endfunction
command! -nargs=* Summarize call Summarize(<f-args>)

