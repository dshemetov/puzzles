;;;; 5. https://adventofcode.com/2024/day/5

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

(defparameter *blank-line* (format nil "~%~%"))

(defun paragraphs (s)
  "The pieces of S between blank lines."
  (loop with end = (length s)
        with start = 0
        for pos = (search *blank-line* s :start2 start)
        collect (subseq s start (or pos end))
        while pos
        do (setf start (+ pos 2))))

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

(deftype order () '(simple-array bit (* *)))

(defun parse-input (s)
  "The rules as a bit matrix, where a 1 at (X, Y) means X must precede Y,
and the updates as vectors of page numbers."
  (destructuring-bind (rules-text updates-text) (paragraphs (trim s))
    (let* ((rules (parse-ints rules-text))
           (size (1+ (reduce #'max rules)))
           (order (make-array (list size size) :element-type 'bit :initial-element 0)))
      (loop for (x y) on rules by #'cddr
            do (setf (aref order x y) 1))
      (values order
              (loop for line in (lines updates-text)
                    collect (coerce (parse-ints line) 'simple-vector))))))

(defun orderedp (update order)
  "Is every page of UPDATE ahead of every page after it?"
  (declare (type simple-vector update) (type order order))
  (loop for i below (length update)
        always (loop for j from (1+ i) below (length update)
                     always (= 1 (aref order (svref update i) (svref update j))))))

(defun reorder (update order)
  "Swap any pair the rules put the other way round. The rules are a total
order on the pages of a single update, so one pass over all pairs sorts it."
  (declare (type simple-vector update) (type order order))
  (loop for i below (length update)
        do (loop for j from (1+ i) below (length update)
                 when (= 1 (aref order (svref update j) (svref update i)))
                   do (rotatef (svref update i) (svref update j))))
  update)

(defun middle (update)
  (svref update (floor (length update) 2)))

(defun part-a (s)
  (multiple-value-bind (order updates) (parse-input s)
    (loop for update in updates
          when (orderedp update order)
            sum (middle update))))

(defun part-b (s)
  (multiple-value-bind (order updates) (parse-input s)
    (loop for update in updates
          unless (orderedp update order)
            sum (middle (reorder update order)))))

(defparameter *test-string* "
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
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
