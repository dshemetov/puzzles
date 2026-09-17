;;;; 1. https://adventofcode.com/2024/day/1

(declaim (optimize (speed 3) (safety 1)))

(defun trim (s)
  "Drop the blank lines that wrap every puzzle input."
  (string-trim '(#\Newline #\Return) s))

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

(defun parse-lists (s)
  "The two columns of the input, as separate vectors."
  (let* ((nums (parse-ints (trim s)))
         (count (floor (length nums) 2))
         (left (make-array count :element-type 'fixnum))
         (right (make-array count :element-type 'fixnum)))
    (loop for (l r) on nums by #'cddr
          for i from 0
          do (setf (aref left i) l
                   (aref right i) r))
    (values left right)))

(defun part-a (s)
  (multiple-value-bind (left right) (parse-lists s)
    (setf left (sort left #'<)
          right (sort right #'<))
    (loop for l across left
          for r across right
          sum (abs (- l r)))))

(defun part-b (s)
  (multiple-value-bind (left right) (parse-lists s)
    (let ((counts (make-hash-table :test #'eql :size (length right))))
      (loop for r across right do (incf (gethash r counts 0)))
      (loop for l across left sum (* l (gethash l counts 0))))))

(defparameter *test-string* "
3   4
4   3
2   5
1   3
3   9
3   3
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
