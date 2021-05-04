
Golang is designed as a simple language that anyone can understand; and it is to some extent. But here are the reasons why, in my opinion, it didn't nail simplicity.

Note that this isn't saying _Golang is bad_. Because it's not. Like every other language, it has flaws, and I'm just trying to address some of them.


## 1. Package Management

At the beginning of Go, there was `GOPATH`. `GOPATH` is an environment variable signifying the package path, i.e. where should Go look for packages. For example, in this code:

``` go
import "something/somepackage"

func main() {
    somepackage.DoSomething()
}
```

Go would look inside every `GOPATH` entry, and check for `src/something`. If it exists, it would bring that in.

I'm not seeing anything "simple" about this. To me, this is just a constraint, _you need to place all your code in a certain place_. I guess they saw the problem with it, because they later added modules.

Go modules ditched `GOPATH` and instead opted for something else: each project has a file called `go.mod`, which contains your dependencies and your module's name. This is a **big** improvement.

But that's not what bothers me. The reason I don't like Go's package management is because of the way you pull in dependencies from the internet. If you have a project, let's call it `foo`, the module's import paths need to _match the URL_. So if you'd publish your module on `https://github.com/bar/foo`, your package name has to be `github.com/bar/foo`, otherwise you can't pull it in from other projects.

**So, what's a better solution?**

A better solution would be to just not care about where the project is hosted. Just import it with whatever name you want. So, in the `go.mod`, you could have something like this:

``` gomod
somethingelseentirely = https://github.com/bar/foo.git
```

So what Go would do is download the repository at that URL and bind it to `somethingelseentirely`. So instead of importing like this

``` go
import "github.com/bar/foo/package"
```

You'd import like this

``` go
import "somethingelseentirely/package"
```

This is both easier to understand, and easier to write code with (not everybody uses an IDE which would autocomplete weird GitHub usernames).



## 2. Interfaces (and `interface{}`)

Interfaces in Go are a nice way of expressing a set of functions that a structure should implement. Here's an example:

``` go
type CommunicationDevice interface {
    SendMessage(msg Message)
}

type Fax struct {
}

func (fax *Fax) SendMessage(msg Message) {
    // Send the message
}
```

With the example above, you can pass a `*Fax` to a function of type `func Something(device CommunicationDevice)`. This is very straightforward, and it's a really useful feature of Go.

But they're also kind of abused.

Go is a strongly typed language that lacks unions, inheritance and sum types. This is a _massive_ flaw in my opinion.

So let's say you were to write an AST node type. In Rust, you can use enums (aka sum types):

``` rust
enum AstNode {
    VariableAccess(String),
    IntLiteral(i64),
}
```

In C, you would use unions (or a hacky inheritance implementation):

``` c
enum AstNodeKind {
    AST_NODE_KIND_VAR_ACCESS,
    AST_NODE_KIND_INT_LITERAL,
};

struct AstNode {
    enum AstNodeKind kind;

    union {
        String valVariableAccess;
        i64 valIntLiteral;
    };
};
```

And in C++ you'd use either unions or inheritance, but I'm not going to show it here, since it's pretty straightforward.

So then, how would you implement that in Go? The first thing that comes to mind is using an interface, like so:

``` go
type AstNode interface {
    NodeKind() AstNodeKind
}
```

Where `AstNodeKind` is an enum (actually this is another thing with Go, they don't exist, so you'd use (type-unsafe) constants). However, most people don't do this. Let's look at the official implementation of the `Token` in `go/xml`:

``` go
type Token interface{}
```

If you're not aware, `interface{}` is basically like a `void*` in C: it can hold **anything**. Zero type checking. You can pass **anything** to a function receiving a token. The way you differentiate between the types is using Go's reflection, you can basically switch over the underlying type of an interface. It's so easy to pass something different to a function and it's very hard to debug. The worst thing though is that this is a very widespread idea in the Go community.

Another place where this is used is generics, which Go doesn't have. Thankfully though, generics in Go are in the works.


## 3. Capitalization

The way Go differentiates between public and private functions or types is using... capitalization? That's right, if the name begins with a capital letter it's public, otherwise it's private.

_What?_

This is so unintuitive. There's nothing simple in this. It's just another constraint. I'm sure users will understand a simple `pub` and `priv`. This "feature" is just a source of confusion in my opinion.



## 4. Strictness of the Compiler

Some of the errors that the compiler generates (which you _can't_ turn off) are just plain annoying. An example is unused imports. Picture this: I just wrote a new type in a new package and I want to see if it compiles. So I go into another package and do

``` go
import "newpackage"
[...]
func something() {
    x := newpackage.SomeType {
        // Initialize this
    }
}
```

I try running it and

``` text
./prog.go:132:2: x declared but not used
```

Just don't. Isn't a warning enough? There _isn't even a way to turn it off_. The same goes for imports (although I can't really argue about that since `gofmt` takes care of it). Sure, unused variables are a source of bugs, but I'm sure a warning is enough. If I choose to ignore it it's my problem, not the compiler's.



## What it _did_ get right

Besides having all the problems I discussed above, I think Go got a lot of things right. Here's a small subset of them:

- **Standard Library** - It's very complete, it provides different parsers, a web server, a templating engine, containers and much more
- **Reflection** - It's just awesome. You can use it for things ranging from printing structures to parsing! (for real check out the XML, JSON, etc parsers from the standard library).
- **Tooling** - In my experience, the Go tools have been really nice to use. The formatter (`gofmt`), the language server (`gopls`) are one of the best ones I've seen.
- **Speed** - By this I mean the compilation speed, Go is one of the fastest compilers I've used. It's really amazing to have a edit-run cycle that's _this_ fast.
- **Multiple Return Types & Error Handling** - This is really nice. Along with the result, your function can return an error that could've happened



## Conclusion

I think Go doesn't really _know_ what it wants to be. On one hand it's supposed to be safe, but we've got `interface{}` everywhere. On the other hand, it's supposed to be simple, but it's got unintuitive stuff like capitalization. It's supposed to be easy to write but it doesn't compile at all if a variable is unused.

At the same time, it has really cool things that are just a joy to use, and not a lot of other languages have them. The syntax is one of the things that it _did_ manage to make simple for example, it's really enjoyable and there's not much boilerplate generally.

I definitely recommend learning Go, even if you don't think you're gonna use it. It doesn't take you more than a few hours to learn 99% of the features, and it will probably prove itself useful one day :)
