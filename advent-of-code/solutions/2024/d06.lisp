;;;; 6. https://adventofcode.com/2024/day/6

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

(defun char-grid (s)
  "S as a 2-D character array, plus its row and column counts.
Short rows are padded with dots so the array stays rectangular."
  (let* ((rows (lines (trim s)))
         (m (length rows))
         (n (reduce #'max rows :key #'length))
         (grid (make-array (list m n) :element-type 'character
                                      :initial-element #\.)))
    (loop for row in rows
          for i from 0
          do (loop for c across row
                   for j from 0
                   do (setf (aref grid i j) c)))
    (values grid m n)))

(deftype grid () '(simple-array character (* *)))

(deftype index ()
  "A row or column of the map, or one step past its edge. The bound is what
keeps LOOPS-P packing its (cell, direction) state with fixnum arithmetic."
  '(integer -1 4096))

;; Directions are numbered 0-3 clockwise from up, so turning right adds one.
(declaim (inline direction turn-right))

(defun direction (d)
  "Row and column deltas for up, right, down, left."
  (ecase d
    (0 (values -1 0))
    (1 (values 0 1))
    (2 (values 1 0))
    (3 (values 0 -1))))

(defun turn-right (d)
  (logand (1+ d) 3))

(defun parse-map (s)
  "The map, its dimensions, and where the guard starts."
  (multiple-value-bind (grid m n) (char-grid s)
    (loop for i below m
          do (loop for j below n
                   when (char= (aref grid i j) #\^)
                     do (setf (aref grid i j) #\.)
                        (return-from parse-map (values grid m n i j))))
    (error "no guard on the map")))

(defun patrol (grid m n start-i start-j)
  "Every cell the guard walks before leaving, in order of first visit."
  (declare (type grid grid) (type index m n start-i start-j))
  (let ((visited (make-array (list m n) :element-type 'bit :initial-element 0))
        (path '())
        (i start-i)
        (j start-j)
        (d 0))
    (declare (type index i j) (type (integer 0 3) d))
    (loop while (and (< -1 i m) (< -1 j n))
          do (when (zerop (aref visited i j))
               (setf (aref visited i j) 1)
               (push (cons i j) path))
             (multiple-value-bind (di dj) (direction d)
               (let ((next-i (+ i di))
                     (next-j (+ j dj)))
                 (if (and (< -1 next-i m) (< -1 next-j n)
                          (char= (aref grid next-i next-j) #\#))
                     (setf d (turn-right d))
                     (setf i next-i j next-j)))))
    (nreverse path)))

(defun loops-p (grid m n start-i start-j obstacle-i obstacle-j seen)
  "Does an extra obstacle trap the guard in a cycle?
SEEN holds one bit per (cell, direction) state and is cleared on entry; a state
reached twice is a cycle. The caller passes it in so it is allocated once."
  (declare (type grid grid) (type simple-bit-vector seen)
           (type index m n start-i start-j obstacle-i obstacle-j))
  (fill seen 0)
  (let ((i start-i) (j start-j) (d 0))
    (declare (type index i j) (type (integer 0 3) d))
    (loop
      (unless (and (< -1 i m) (< -1 j n)) (return nil))
      (let ((state (+ (* 4 (+ (* i n) j)) d)))
        (when (= 1 (sbit seen state)) (return t))
        (setf (sbit seen state) 1))
      (multiple-value-bind (di dj) (direction d)
        (let ((next-i (+ i di))
              (next-j (+ j dj)))
          (if (and (< -1 next-i m) (< -1 next-j n)
                   (or (and (= next-i obstacle-i) (= next-j obstacle-j))
                       (char= (aref grid next-i next-j) #\#)))
              (setf d (turn-right d))
              (setf i next-i j next-j)))))))

(defun part-a (s)
  (multiple-value-bind (grid m n start-i start-j) (parse-map s)
    (length (patrol grid m n start-i start-j))))

(defun part-b (s)
  "Only a cell the guard already walks can change the route, so the original
patrol is the whole candidate set."
  (multiple-value-bind (grid m n start-i start-j) (parse-map s)
    (let ((seen (make-array (* m n 4) :element-type 'bit :initial-element 0)))
      (loop for (i . j) in (patrol grid m n start-i start-j)
            unless (and (= i start-i) (= j start-j))
              count (loops-p grid m n start-i start-j i j seen)))))

(defparameter *test-string* "
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
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
