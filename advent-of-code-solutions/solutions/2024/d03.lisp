;;;; 3. https://adventofcode.com/2024/day/3

(declaim (optimize (speed 3) (safety 1)))

(defun trim (s)
  "Drop the blank lines that wrap every puzzle input."
  (string-trim '(#\Newline #\Return) s))

(defun scan-integer (s start end)
  "The run of digits starting at START, and the index just past it.
NIL when START does not hold a digit."
  (let ((i start))
    (loop while (and (< i end) (digit-char-p (char s i))) do (incf i))
    (when (> i start)
      (values (parse-integer s :start start :end i) i))))

(defun mul-at (s start end)
  "The product of the mul(x,y) whose arguments start at START, or NIL.
START points just past the opening \"mul(\"."
  (multiple-value-bind (x after-x) (scan-integer s start end)
    (when (and x (< after-x end) (char= (char s after-x) #\,))
      (multiple-value-bind (y after-y) (scan-integer s (1+ after-x) end)
        (when (and y (< after-y end) (char= (char s after-y) #\)))
          (* x y))))))

(defun prefix-at-p (prefix s i)
  (let ((end (+ i (length prefix))))
    (and (<= end (length s))
         (string= prefix s :start2 i :end2 end))))

(defun part-a (s)
  (let* ((s (trim s))
         (end (length s)))
    (loop with total = 0
          with i = 0
          for pos = (search "mul(" s :start2 i :end2 end)
          while pos
          do (incf total (or (mul-at s (+ pos 4) end) 0))
             (setf i (+ pos 4))
          finally (return total))))

(defun part-b (s)
  "One pass, tracking whether do() or don't() last switched the multiplier on."
  (let* ((s (trim s))
         (end (length s))
         (total 0)
         (enabled t)
         (i 0))
    (loop while (< i end)
          do (cond ((prefix-at-p "do()" s i)
                    (setf enabled t)
                    (incf i 4))
                   ((prefix-at-p "don't()" s i)
                    (setf enabled nil)
                    (incf i 7))
                   ((prefix-at-p "mul(" s i)
                    (let ((product (mul-at s (+ i 4) end)))
                      (when (and enabled product) (incf total product)))
                    (incf i 4))
                   (t (incf i))))
    total))

(defparameter *test-string* "
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
")

(defparameter *test-string-2* "
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
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
