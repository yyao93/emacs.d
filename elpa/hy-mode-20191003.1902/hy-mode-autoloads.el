;;; hy-mode-autoloads.el --- automatically extracted autoloads
;;
;;; Code:
(add-to-list 'load-path (directory-file-name (or (file-name-directory #$) (car load-path))))

;;;### (autoloads nil "hy-jedhy" "hy-jedhy.el" (23990 17054 895813
;;;;;;  500000))
;;; Generated autoloads from hy-jedhy.el

(autoload 'run-jedhy "hy-jedhy" "\
Startup internal Hy interpreter process, enabling jedhy for `company-mode'.

\(fn)" t nil)

;;;***

;;;### (autoloads nil "hy-mode" "hy-mode.el" (23990 17054 893798
;;;;;;  44000))
;;; Generated autoloads from hy-mode.el

(autoload 'hy-mode "hy-mode" "\
Major mode for editing Hy files.

\(fn)" t nil)

(autoload 'hy-insert-pdb "hy-mode" "\
Import and set pdb trace at point.

\(fn)" t nil)

;;;***

;;;### (autoloads nil "hy-shell" "hy-shell.el" (23990 17054 899559
;;;;;;  258000))
;;; Generated autoloads from hy-shell.el

(autoload 'inferior-hy-mode "hy-shell" "\
Major mode for Hy inferior process.

\(fn)" t nil)

(autoload 'run-hy "hy-shell" "\
Startup and/or switch to a Hy interpreter process.

\(fn)" t nil)

;;;***

;;;### (autoloads nil nil ("hy-base.el" "hy-font-lock.el" "hy-mode-pkg.el")
;;;;;;  (23990 17054 897616 885000))

;;;***

;; Local Variables:
;; version-control: never
;; no-byte-compile: t
;; no-update-autoloads: t
;; End:
;;; hy-mode-autoloads.el ends here
