;;;; 9. https://adventofcode.com/2024/day/9

(declaim (optimize (speed 3) (safety 1)))

(defun trim (s)
  "Drop the blank lines that wrap every puzzle input."
  (string-trim '(#\Newline #\Return) s))

(deftype offsets ()
  "Block offsets and lengths on the disk."
  '(simple-array fixnum (*)))

(defun disk-map (s)
  "The input digits: even entries are file lengths, odd ones are gap lengths."
  (let* ((s (trim s))
         (sizes (make-array (length s) :element-type 'fixnum)))
    (loop for c across s
          for i from 0
          do (setf (aref sizes i) (or (digit-char-p c) 0)))
    sizes))

(defun checksum-of-disk (disk)
  (declare (type offsets disk))
  (loop for position below (length disk)
        for id = (aref disk position)
        unless (= id -1)
          sum (* position id)))

(defun part-a (s)
  "Blocks move one at a time, so the disk can be laid out and compacted in place."
  (let* ((sizes (disk-map s))
         (blocks (reduce #'+ sizes))
         (disk (make-array blocks :element-type 'fixnum :initial-element -1)))
    (declare (type offsets sizes disk) (type fixnum blocks))
    (loop with position of-type fixnum = 0
          for i below (length sizes)
          for size = (aref sizes i)
          do (when (evenp i)
               (fill disk (floor i 2) :start position :end (+ position size)))
             (incf position size))
    ;; Walk a pointer in from each end, moving the rightmost block into the
    ;; leftmost gap, until the two meet.
    (let ((left 0) (right (1- blocks)))
      (declare (type fixnum left right))
      (loop
        (loop while (and (< left blocks) (/= (aref disk left) -1)) do (incf left))
        (loop while (and (>= right 0) (= (aref disk right) -1)) do (decf right))
        (when (>= left right) (return))
        (setf (aref disk left) (aref disk right)
              (aref disk right) -1)
        (incf left)
        (decf right)))
    (checksum-of-disk disk)))

(defun part-b (s)
  "Whole files move, so only their positions change. Tracking the files and the
gaps as lengths avoids laying out the disk at all."
  (let* ((sizes (disk-map s))
         (entries (length sizes))
         (files (ceiling entries 2))
         (file-position (make-array files :element-type 'fixnum :initial-element 0))
         (file-size (make-array files :element-type 'fixnum :initial-element 0))
         (gap-position (make-array (floor entries 2) :element-type 'fixnum :initial-element 0))
         (gap-size (make-array (floor entries 2) :element-type 'fixnum :initial-element 0))
         (gaps 0))
    (declare (type offsets sizes file-position file-size gap-position gap-size)
             (type fixnum entries files gaps))
    (loop with position of-type fixnum = 0
          for i below entries
          for size of-type fixnum = (aref sizes i)
          do (if (evenp i)
                 (setf (aref file-position (floor i 2)) position
                       (aref file-size (floor i 2)) size)
                 (progn
                   (setf (aref gap-position gaps) position
                         (aref gap-size gaps) size)
                   (incf gaps)))
             (incf position size))
    ;; Try each file once, highest id first, in the leftmost gap that holds it.
    ;; A gap shrinks by what it takes; one used up reaches size 0 and fits nothing.
    (loop for id from (1- files) downto 0
          for size of-type fixnum = (aref file-size id)
          do (loop for g below gaps
                   while (< (aref gap-position g) (aref file-position id))
                   when (>= (aref gap-size g) size)
                     do (setf (aref file-position id) (aref gap-position g))
                        (incf (aref gap-position g) size)
                        (decf (aref gap-size g) size)
                        (return)))
    (loop for id below files
          sum (loop for offset below (aref file-size id)
                    sum (* id (+ (aref file-position id) offset))))))

(defparameter *test-string* "
2333133121414131402
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
