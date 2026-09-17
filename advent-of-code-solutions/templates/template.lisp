;;;; @URL@

(declaim (optimize (speed 3) (safety 1)))

(defun split-on (s char)
  "The pieces of S between occurrences of CHAR."
  (loop with end = (length s)
        with start = 0
        for pos = (position char s :start start)
        collect (subseq s start (or pos end))
        while pos
        do (setf start (1+ pos))))

(defun lines (s)
  (split-on (string-trim '(#\Newline #\Return) s) #\Newline))

(defun part-a (s)
  (declare (ignorable s))
  0)

(defun part-b (s)
  (declare (ignorable s))
  0)

(defparameter *example* "
")

(defun read-file (path)
  (with-open-file (in path :external-format :utf-8)
    (let ((buffer (make-string (file-length in))))
      (subseq buffer 0 (read-sequence buffer in)))))

(defun seconds ()
  (/ (get-internal-real-time) (float internal-time-units-per-second 1d0)))

(defun main ()
  (let ((s (read-file (second sb-ext:*posix-argv*))))
    (dolist (part '(part-a part-b))
      (let* ((start (seconds))
             (answer (funcall part s)))
        (format t "~A~%" answer)
        (format *error-output* "~(~A~): ~,4Fs~%" part (- (seconds) start))))))

(main)
