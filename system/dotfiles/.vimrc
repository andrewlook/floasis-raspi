vnoremap <C-r> "hy:%s/<C-r>h//gc<left><left><left>

let g:go_version_warning = 0

" {{{ Vundle config }}}
""" from: https://github.com/gmarik/Vundle.vim
"""
set nocompatible
filetype off
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

" let Vundle manage Vundle
" required! 
Plugin 'gmarik/Vundle.vim'
Plugin 'scrooloose/syntastic'
Plugin 'scrooloose/nerdtree'
Plugin 'Lokaltog/vim-powerline'
Plugin 'kien/ctrlp.vim'
Plugin 'godlygeek/tabular'
Plugin 'fatih/vim-go'
Plugin 'mitsuhiko/vim-jinja'
Plugin 'junegunn/goyo.vim'
Plugin 'junegunn/seoul256.vim'
Plugin 'junegunn/limelight.vim'
Plugin 'rking/ag.vim'
Plugin 'ghewgill/vim-scmdiff'
Plugin 'tmhedberg/SimpylFold'
Plugin 'vim-scripts/indentpython.vim'
call vundle#end()
filetype plugin indent on

" To ignore plugin indent changes, instead use:
"filetype plugin on
""
" Brief help
" " :PluginList       - lists configured plugins
" " :PluginInstall    - installs plugins; append `!` to update or just
" :PluginUpdate
" " :PluginSearch foo - searches for foo; append `!` to refresh local cache
" " :PluginClean      - confirms removal of unused plugins; append `!` to
" auto-approve removal
" "
" " see :h vundle for more details or wiki for FAQ
" " Put your non-Plugin stuff after this line
"
"""
""" End Vundle configs
"""
" {{{ Colors }}}
" http://emerg3nc3.wordpress.com/2012/07/28/full-256-color-support-for-vim-andor-xterm-on-ubuntu-12-04/
set t_Co=256

colo seoul256

syntax on


" {{{ Spaces & Tabs

set expandtab " always uses spaces instead of tab characters
set tabstop=4 " size of a hard tabstop
set shiftwidth=4 " size of an "indent"
set softtabstop=4

" to make backspace key work in insert mode: http://vim.wikia.com/wiki/Backspace_and_delete_problems
set backspace=2


" {{{ UI Config

set number " show line numbers
set showcmd " show command in bottom bar
set cursorline "highlight current line
set laststatus=2 " Enable vim-powerline's status bar
set wildmenu
set showmatch


" {{{ Folds }}}

" Enable folding
set foldmethod=indent
set foldlevel=99

" comma opens/closes folds
nnoremap , za


" {{{ Buffers }}}

" save & load view folds automatically: http://vim.wikia.com/wiki/Make_views_automatic
autocmd BufWinLeave *.* mkview
autocmd BufWinEnter *.* silent loadview 



" {{{ Movement }}}

inoremap jk <ESC>

" move vertically by visual line
nnoremap j gj
nnoremap k gk

" highlight last inserted text
nnoremap gV `[v`]

" split navigations
"
" nnoremap remaps one key combination to another. The no part means remap the
" key in normal mode as opposed to visual mode. Basically, nnoremap <C-J>
" <C-W><C-j> says, in normal mode when I hit <C-J>, do <C-W><C-j> instead.
" More info can be found here:
" - https://stackoverflow.com/questions/3776117/what-is-the-difference-between-the-remap-noremap-nnoremap-and-vnoremap-mapping
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>

" {{{ Leader Commands }}}
let mapleader="\<Space>" "leader is space

" Silver Searcher
" ---------------
" e    to open file and close the quickfix window
" o    to open (same as enter)
" go   to preview file (open but maintain focus on ag.vim results)
" t    to open in new tab
" T    to open in new tab silently
" h    to open in horizontal split
" H    to open in horizontal split silently
" v    to open in vertical split
" gv   to open in vertical split silently
" q    to close the quickfix window
nnoremap <leader>a :Ag<space>

" {{{ Searching }}}

set incsearch " search as characters are entered
set hlsearch " highlight matches

" turn off search highlight using `<SPACE>-`
nnoremap <leader>- :nohlsearch<CR>
" {{{ CtrlP }}}
let g:ctrlp_match_window = 'bottom,order:ttb'
let g:ctrlp_switch_buffer = 0
let g:ctrlp_working_path_mode = 0
let g:ctrlp_user_command = 'ag %s -l --nocolor --hidden -g ""'

" {{{ Tmux }}}
" allows cursor change in tmux mode
if exists('$TMUX')
    let &t_SI = "\<Esc>Ptmux;\<Esc>\<Esc>]50;CursorShape=1\x7\<Esc>\\"
    let &t_EI = "\<Esc>Ptmux;\<Esc>\<Esc>]50;CursorShape=0\x7\<Esc>\\"
else
    let &t_SI = "\<Esc>]50;CursorShape=1\x7"
    let &t_EI = "\<Esc>]50;CursorShape=0\x7"
endif
" {{{ Backups }}}
set backup
set backupdir=~/.vim-tmp,~/.tmp,~/tmp,/var/tmp,/tmp
set backupskip=/tmp/*,/private/tmp/*
set directory=~/.vim-tmp,~/.tmp,~/tmp,/var/tmp,/tmp
set writebackup


autocmd User GoyoEnter Limelight
autocmd User GoyoEnter Limelight!

" {{{ Syntastic }}}
" Pointers here on how to make it less invasive:
" - https://vivekanandxyz.wordpress.com/2017/08/16/using-syntastic-for-python-development/

" show list of errors and warnings on the current file
nmap <leader>e :Errors<CR>

let g:syntastic_check_on_open=0
let g:syntastic_check_on_wq = 0
let g:syntastic_mode_map={'mode':'passive'}
:command Sc :SyntasticCheck
let g:syntastic_python_checkers=['pylint']
let g:syntastic_javascript_checkers=['eslint']

" YouCompleteMe
let g:ycm_autoclose_preview_window_after_completion=1
map <leader>g  :YcmCompleter GoToDefinitionElseDeclaration<CR>


" Pep8
au BufNewFile,BufRead *.py
    \ set tabstop=4 |
    \ set softtabstop=4 |
    \ set shiftwidth=4 |
    \ set textwidth=79 |
    \ set expandtab |
    \ set autoindent |
    \ set fileformat=unix

" fullstack
au BufNewFile,BufRead *.js,*.html,*.css,*.scss
    \ set tabstop=2 |
    \ set softtabstop=2 |
    \ set shiftwidth=2
