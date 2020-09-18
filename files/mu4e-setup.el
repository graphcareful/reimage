;; example configuration for mu4e
(require 'mu4e)

;; use mu4e for e-mail in emacs
(setq mail-user-agent 'mu4e-user-agent)

;; the next are relative to the root maildir
;; (see `mu info`).
;; instead of strings, they can be functions too, see
;; their docstring or the chapter 'Dynamic folders'
(setq mu4e-sent-folder   "/Gmail/[Gmail].Sent Mail"
      mu4e-drafts-folder "/Gmail/[Gmail].Drafts"
      mu4e-trash-folder  "/Gmail/[Gmail].Trash")

;; the maildirs you use frequently; access them with 'j' ('jump')
(setq mu4e-maildir-shortcuts
      '((:maildir "/Gmail/inbox"             :key ?i)
        (:maildir "/Gmail/v-dev"             :key ?v)
        (:maildir "/Gmail/v-dev.me"          :key ?m)
        (:maildir "/Gmail/[Gmail].Sent Mail" :key ?s)))

;; the headers to show in the headers list -- a pair of a field
;; and its width, with `nil' meaning 'unlimited'
;; (better only use that for the last field.
;; These are the defaults:
(setq mu4e-headers-fields
      '( (:date          .  25)    ;; alternatively, use :human-date
         (:flags         .   6)
         (:from          .  22)
         (:subject       .  nil))) ;; alternatively, use :thread-subject

;; program to get mail; alternatives are 'fetchmail', 'getmail'
;; isync or your own shellscript. called when 'U' is pressed in
;; main view.

;; If you get your mail without an explicit command,
;; use "true" for the command (this is the default)
(setq mu4e-get-mail-command "offlineimap -o")

;; general emacs mail settings; used when composing e-mail
;; the non-mu4e-* stuff is inherited from emacs/message-mode
(setq mu4e-compose-reply-to-address "rob@vectorized.io"
      user-mail-address "rob@vectorized.io"
      user-full-name "Rob Blafford")
;; (setq mu4e-compose-signature "Rob Blafford\nvectorized.io\n")

(setq mu4e-contexts
      `( ,(make-mu4e-context
	         :name "Work"
	         :enter-func (lambda () (mu4e-message "Entering Work email context"))
           :leave-func (lambda () (mu4e-message "Leaving Work email context"))
	         :match-func (lambda (msg)
			                   (when msg
			                     (mu4e-message-contact-field-matches msg :to "rob@vectorized.io")))
	         :vars '((user-mail-address	. "rob@vectorized.io")
		               (user-full-name	  . "Rob Blafford")))))


;; set `mu4e-context-policy` and `mu4e-compose-policy` to tweak when mu4e should
;; guess or ask the correct context, e.g.

;; start with the first (default) context;
;; default is to ask-if-none (ask when there's no context yet, and none match)
(setq mu4e-context-policy 'pick-first)

;; compose with the current context is no context matches;
;; default is to ask
(setq mu4e-compose-context-policy 'pick-first)

;; send mail settings
(setq
 send-mail-function 'smtpmail-send-it
 message-send-mail-function 'smtpmail-send-it
 smtpmail-starttls-credentials '(("smtp.gmail.com" "587" nil nil))
 smtpmail-auth-credentials (expand-file-name "~/.authinfo")
 smtpmail-default-smtp-server "smtp.gmail.com"
 smtpmail-smtp-server "smtp.gmail.com"
 smtpmail-smtp-service 587
 smtpmail-debug-info t
 starttls-extra-arguments nil
 starttls-gnutls-program "/usr/bin/gnutls-cli"
 starttls-extra-arguments nil
 starttls-use-gnutls t

 ;; if you need offline mode, set these -- and create the queue dir
 ;; with 'mu mkdir', i.e.. mu mkdir /home/user/Maildir/queue
 smtpmail-queue-mail  nil
 smtpmail-queue-dir  "/home/robert/Maildir/queue/cur")

;; don't keep message buffers around
(setq message-kill-buffer-on-exit t)

