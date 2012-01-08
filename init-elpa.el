(defun require-package (package &optional min-version no-refresh)
  "Ask elpa to install given PACKAGE."
  (unless (package-installed-p package min-version)
    (if (or (assoc package package-archive-contents) no-refresh)
        (package-install package)
      (progn
        (package-refresh-contents)
        (require-package package min-version t)))))

;; When switching between Emacs 23 and 24, we always use the bundled package.el in Emacs 24
(let ((package-el-site-lisp-dir (expand-file-name "~/.emacs.d/site-lisp/package")))
  (when (and (file-directory-p package-el-site-lisp-dir)
             (> emacs-major-version 23))
    (message "Removing local package.el from load-path to avoid shadowing bundled version")
    (setq load-path (remove package-el-site-lisp-dir load-path))))

(require 'package)
(add-to-list 'package-archives '("marmalade" . "http://marmalade-repo.org/packages/"))
(add-to-list 'package-archives '("tromey" . "http://tromey.com/elpa/"))

(package-initialize)

(require-package 'ido-ubiquitous)
(when (< emacs-major-version 24)
  (require-package 'color-theme))
(require-package 'erc)
(require-package 'fringe-helper)
(require-package 'gnuplot)
(require-package 'haskell-mode)
(when *vi-emulation-support-enabled*
  (require-package 'highlight-symbol))
(require-package 'flymake-cursor)
(require-package 'json)
(require-package 'js2-mode)
(require-package 'lua-mode)
(require-package 'project-local-variables)
(require-package 'ruby-mode)
(require-package 'inf-ruby)
(require-package 'yari)
(require-package 'rvm)
(require-package 'yaml-mode)
(require-package 'paredit)
(require-package 'eldoc-eval)
(require-package 'slime)
(require-package 'slime-fuzzy)
(require-package 'slime-repl)
(require-package 'gist)
(require-package 'haml-mode)
(require-package 'sass-mode)
(require-package 'elein)
(require-package 'durendal)
(require-package 'markdown-mode)
(require-package 'smex)
(require-package 'rainbow-mode)
(require-package 'maxframe)
(when (< emacs-major-version 24)
  (require-package 'org))
(require-package 'clojure-mode)
(require-package 'clojure-test-mode)
(require-package 'diminish)
(require-package 'autopair)
(require-package 'js-comint)
(require-package 'php-mode)
(require-package 'scratch)
(require-package 'mic-paren)
(require-package 'rainbow-delimiters)
(require-package 'marmalade)

;; I maintain this chunk:
(require-package 'ac-slime)
(require-package 'vc-darcs)
(require-package 'color-theme-sanityinc-solarized)
(require-package 'color-theme-sanityinc-tomorrow)
(require-package 'session)
(require-package 'tidy)
(require-package 'whole-line-or-region)
(require-package 'flymake-ruby)
(require-package 'flymake-haml)
(require-package 'flymake-sass)
(require-package 'flymake-shell)
(require-package 'flymake-php)
(require-package 'flymake-coffee)
(require-package 'flymake-jslint)
(require-package 'flymake-css)
(require-package 'ibuffer-vc)
(require-package 'coffee-mode)
(require-package 'elisp-slime-nav)
(require-package 'hippie-expand-slime)
(require-package 'mwe-log-commands)
(require-package 'move-text)
(require-package 'less-css-mode)
(require-package 'hl-sexp)
(require-package 'dsvn)
(require-package 'crontab-mode)
(require-package 'regex-tool)
(require-package 'rinari)
(require-package 'ruby-compilation)
(require-package 'iy-go-to-char)

(provide 'init-elpa)
