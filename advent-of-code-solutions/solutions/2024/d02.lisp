;;;; 2. https://adventofcode.com/2024/day/2

(declaim (optimize (speed 3) (safety 1)))

(defun trim (s)
  "Drop the blank lines that wrap every puzzle input."
  (string-trim '(#\Newline #\Return) s))

(defun split-on (s char)
  "The pieces of S between occurrences of CHAR."
  (loop with end = (length s)
        with start = 0
        for pos = (position char s :start start)
        collect (subseq s start (or pos end))
        while pos
        do (setf start (1+ pos))))

(defun lines (s)
  (split-on s #\Newline))

(defun parse-ints (s)
  "Every run of digits in S, in order. Signs and decimal points are ignored."
  (let ((result '())
        (i 0)
        (n (length s)))
    (loop while (< i n)
          do (if (digit-char-p (char s i))
                 (multiple-value-bind (value end)
                     (parse-integer s :start i :junk-allowed t)
                   (push value result)
                   (setf i end))
                 (incf i)))
    (nreverse result)))

(defun parse-report (line)
  (coerce (parse-ints line) '(simple-array fixnum (*))))

(defun safep (levels &optional (skip -1))
  "Is the parse-report safe with the level at index SKIP left out?
Safe means every step moves the same way and lands between 1 and 3."
  (declare (type (simple-array fixnum (*)) levels)
           (type fixnum skip))
  (let ((increasing t)
        (decreasing t)
        (previous nil)
        (kept 0))
    (declare (type fixnum kept))
    (loop for i of-type fixnum below (length levels)
          unless (= i skip)
            do (let ((level (aref levels i)))
                 (incf kept)
                 (when previous
                   (let ((step (- level (the fixnum previous))))
                     (when (or (zerop step) (> (abs step) 3))
                       (return-from safep nil))
                     (if (plusp step)
                         (setf decreasing nil)
                         (setf increasing nil))))
                 (setf previous level)))
    (and (>= kept 2) (or increasing decreasing))))

(defun part-a (s)
  (loop for line in (lines (trim s))
        count (safep (parse-report line))))

(defun part-b (s)
  (loop for line in (lines (trim s))
        for levels = (parse-report line)
        count (or (safep levels)
                  (loop for skip below (length levels)
                        thereis (safep levels skip)))))

(defparameter *test-string* "
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
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
