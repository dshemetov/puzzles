;;;; 7. https://adventofcode.com/2024/day/7

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

(defun shift (n)
  "The power of ten that concatenating N onto another number shifts it by."
  (declare (type fixnum n))
  (loop with scale of-type fixnum = 10
        while (>= n scale)
        do (setf scale (* scale 10))
        finally (return scale)))

(defun reachable-p (target operands index concatp)
  "Can OPERANDS[0..INDEX] make TARGET?
Undoes the last operator instead of trying every combination forwards, so an
operator that cannot have produced TARGET prunes its whole subtree."
  (declare (type (simple-array fixnum (*)) operands)
           (type fixnum target index))
  (if (zerop index)
      (= target (aref operands 0))
      (let ((operand (aref operands index)))
        (or (and (> target operand)
                 (reachable-p (- target operand) operands (1- index) concatp))
            (and (zerop (mod target operand))
                 (reachable-p (floor target operand) operands (1- index) concatp))
            (and concatp
                 (let ((scale (shift operand)))
                   (and (= (mod target scale) operand)
                        (plusp (floor target scale))
                        (reachable-p (floor target scale) operands (1- index) concatp))))))))

(defun total-calibration (s concatp)
  (loop for line in (lines (trim s))
        for numbers = (parse-ints line)
        for operands = (coerce (rest numbers) '(simple-array fixnum (*)))
        when (reachable-p (first numbers) operands (1- (length operands)) concatp)
          sum (first numbers)))

(defun part-a (s)
  (total-calibration s nil))

(defun part-b (s)
  (total-calibration s t))

(defparameter *test-string* "
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
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
