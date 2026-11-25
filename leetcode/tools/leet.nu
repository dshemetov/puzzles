# Helpers behind the Justfile recipes. Run from the leetcode root.
# Recipes load this with `use leet.nu` (the Justfile points NU_LIB_DIRS at tools/).

const BASE = "https://leetcode.com"
const HEADERS = {"User-Agent": "Mozilla/5.0", Referer: "https://leetcode.com"}
const QUESTION_FIELDS = "questionFrontendId title titleSlug difficulty content topicTags { name } stats sampleTestCase"

def pad [n: int]: nothing -> string {
    $n | into string | fill --alignment right --character '0' --width 4
}

def cache-path []: nothing -> string {
    ($env.XDG_CACHE_HOME? | default ($nu.home-dir | path join ".cache")) | path join "leet" "problems.json"
}

# The list of all problems, cached for a day.
def problems []: nothing -> list {
    let path = cache-path
    if ($path | path exists) and ((ls $path).0.modified > (date now) - 1day) {
        return (open $path)
    }
    let all = graphql 'query { problemsetQuestionList: questionList(categorySlug: "", limit: -1, filters: {}) { questions: data { frontendQuestionId: questionFrontendId titleSlug } } }' {}
        | get problemsetQuestionList.questions
        | each {|q| {number: ($q.frontendQuestionId | into int), slug: $q.titleSlug}}
    mkdir ($path | path dirname)
    $all | save --force $path
    $all
}

def slug-for [number: int]: nothing -> string {
    let hit = problems | where number == $number
    if ($hit | is-empty) { error make {msg: $"problem ($number) not found"} }
    $hit.0.slug
}

def graphql [query: string, variables: record]: nothing -> record {
    http post --content-type application/json --headers $HEADERS $"($BASE)/graphql" {query: $query, variables: $variables}
        | get data
}

def question [slug: string]: nothing -> record {
    graphql $"query q\($slug: String!\) { question\(titleSlug: $slug\) { ($QUESTION_FIELDS) } }" {slug: $slug}
        | get question
}

# Problem HTML to plain text: block tags become newlines, other tags go, common entities are decoded.
def strip-html []: string -> string {
    $in
        | str replace --all --regex '<(p|div|li|br|pre|h[1-4]|tr)[^>]*>' "\n"
        | str replace --all --regex '<[^>]*>' ''
        | str replace --all '&nbsp;' ' ' | str replace --all '&lt;' '<' | str replace --all '&gt;' '>'
        | str replace --all '&quot;' '"' | str replace --all '&#39;' "'" | str replace --all '&amp;' '&'
        | str replace --all --regex '\n{3,}' "\n\n"
        | str trim
}

def show [q: record] {
    let stats = $q.stats | from json
    print $"[($q.questionFrontendId)] ($q.title)  \(($q.difficulty)\)"
    print $"URL: ($BASE)/problems/($q.titleSlug)/"
    print $"Tags: ($q.topicTags.name | str join ', ')"
    print $"Accepted: ($stats.totalAccepted)  |  Submissions: ($stats.totalSubmission)  |  Rate: ($stats.acRate)"
    print $"\nSample test case:\n  ($q.sampleTestCase | str replace --all "\n" ' ')\n\n(1..60 | each {"─"} | str join)\n"
    print ($q.content | strip-html)
}

# Numbers of the problems that already have a solution file.
def solved []: nothing -> list<int> {
    glob solutions/p*.py | path basename | each { parse --regex '^p(?<n>\d+)' | get n.0 | into int } | uniq
}

# Print a problem statement; with no number, the smallest unsolved one.
export def problem [number?: int] {
    let n = $number | default (problems | get number | where $it not-in (solved) | sort | first)
    show (question (slug-for $n))
}

# Print today's daily challenge.
export def daily [] {
    let q = graphql 'query { activeDailyCodingChallengeQuestion { question { questionFrontendId title titleSlug difficulty content topicTags { name } stats sampleTestCase } } }' {}
    show $q.activeDailyCodingChallengeQuestion.question
}

# Create solutions/pNNNN.py from the template.
export def new [number: int] {
    let path = $"solutions/p(pad $number).py"
    if ($path | path exists) { error make {msg: $"($path) already exists"} }
    let slug = slug-for $number
    let title = (question $slug).title
    open --raw templates/template.py
        | str replace --all '@N@' ($number | into string)
        | str replace --all '@TITLE@' $title
        | str replace --all '@URL@' $"($BASE)/problems/($slug)/"
        | save $path
    print $path
}
