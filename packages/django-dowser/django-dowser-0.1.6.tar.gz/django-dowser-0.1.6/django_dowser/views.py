import gc
import sys
import threading

from django.template import RequestContext
from django.shortcuts import render
from django.utils.html import escape
from types import ModuleType, FrameType
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import user_passes_test

from . import dowser, DOWSER_NAMES
from . import reftree


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    floor = int(request.GET.get('floor', default=0))
    rows = []
    typenames = sorted(dowser.history.keys())
    for typename in typenames:
        history = dowser.history[typename]
        maxhist = 0
        for hist in history:
            maxhist = max(maxhist, max(hist))
        charts = " ".join(['<img class="chart" src="%s" alt="%s"/>' %
                           (chart_url2(history[x]), DOWSER_NAMES[x])
                           for x in range(len(history))])
        if maxhist > floor:
            row = ('<div class="typecount">%s<br />'
                   '%s<br />'
                   'Cur: %s Max: %s <a href="%s">TRACE</a></div>'
                   % (escape(typename),
                      charts,
                      history[0][0], maxhist,
                      "trace/%s" % typename,
                      )
                   )
            rows.append(row)
    return render(request, "django_dowser/graphs.html",
                  {'output': "\n".join(rows)})


def chart_url2(entries):
    url = ("http://chart.apis.google.com/chart?chs=%sx20&cht=ls&"
           "chco=0077CC&chd=t:%s") % (
               len(entries), ",".join(str(x) for x in reversed(entries)))
    return url


def chart_url(typename, history_slot=0):
    data = reversed(list(dowser.history[typename][history_slot]))  # TODO
    url = chart_url2(data)
    return url


@user_passes_test(lambda u: u.is_superuser)
def trace(request, typename, objid=None):
    gc.collect()

    if objid is None:
        rows = trace_all(typename)
    else:
        rows = trace_one(typename, objid)

    return render(request, "django_dowser/trace.html", {
        'output': "\n".join(rows),
        'typename': typename,
        'objid': objid or "",
    })


@user_passes_test(lambda u: u.is_superuser)
def tree(request, objid, typename):
    gc.collect()

    rows = []
    objid = int(objid)
    all_objs = gc.get_objects()
    for obj in all_objs:
        if id(obj) == objid:
            objtype = type(obj)
            if str(objtype.__module__) + "." + objtype.__name__ != typename:
                rows = ["<h3>The object you requested is no longer "
                        "of the correct type.</h3>"]
            else:
                rows.append('<div class="obj">')

                my_tree = ReferrerTree(obj)
                my_tree.ignore(all_objs)
                for depth, parentid, parentrepr in my_tree.walk(
                        maxresults=1000):
                    rows.append(parentrepr)

                rows.append('</div>')
            break
    if not rows:
        rows = ["<h3>The object you requested was not found.</h3>"]

    return render(request, "django_dowser/tree.html", {
        'output': "\n".join(rows), 'typename': typename, 'objid': objid})


method_types = [
    type(tuple.__le__),                 # 'wrapper_descriptor'
    type([1].__le__),                   # 'method-wrapper'
    type(sys.getcheckinterval),         # 'builtin_function_or_method'
    type(threading.Thread.isAlive),     # 'instancemethod'
]


def trace_all(typename):
    rows = []
    for obj in gc.get_objects():
        objtype = type(obj)
        if str(objtype.__module__) + "." + objtype.__name__ == typename:
            rows.append("<p class='obj'>%s</p>"
                        % ReferrerTree(obj).get_repr(obj))
    if not rows:
        rows = ["<h3>The type you requested was not found.</h3>"]
    return rows


def trace_one(typename, objid):
    rows = []
    objid = int(objid)
    all_objs = gc.get_objects()
    for obj in all_objs:
        if id(obj) == objid:
            objtype = type(obj)
            if str(objtype.__module__) + "." + objtype.__name__ != typename:
                rows = ["<h3>The object you requested is no longer "
                        "of the correct type.</h3>"]
            else:
                tree = ReferrerTree(obj)

                # repr
                rows.append("<p class='obj'>%s</p>" % get_repr(obj, 5000))

                # Attributes
                rows.append('<div class="obj"><h3>Attributes</h3>')
                for k in dir(obj):
                    v = getattr(obj, k)
                    if type(v) not in method_types:
                        rows.append('<p class="attr"><b>%s:</b> %s</p>' %
                                    (k, get_repr(v)))
                    del v
                rows.append('</div>')

                # Referrers
                rows.append('<div class="refs"><h3>Referrers (Parents)</h3>')
                rows.append('<p class="desc"><a href="%s">Show the '
                            'entire tree</a> of reachable objects</p>'
                            % ("../../tree/%s/%s" % (typename, objid)))
                tree.ignore(all_objs)
                for depth, parentid, parentrepr in tree.walk(maxdepth=1):
                    if parentid:
                        rows.append("<p class='obj'>%s</p>" % parentrepr)
                rows.append('</div>')

                # Referents
                rows.append('<div class="refs"><h3>Referents (Children)</h3>')
                for child in gc.get_referents(obj):
                    rows.append("<p class='obj'>%s</p>" % tree.get_repr(child))
                rows.append('</div>')
            break
    if not rows:
        rows = ["<h3>The object you requested was not found.</h3>"]
    return rows


def get_repr(obj, limit=250):
    return escape(reftree.get_repr(obj, limit))


class ReferrerTree(reftree.Tree):

    ignore_modules = True

    def _gen(self, obj, depth=0):
        if self.maxdepth and depth >= self.maxdepth:
            yield depth, 0, "---- Max depth reached ----"
            return
        if isinstance(obj, ModuleType) and self.ignore_modules:
            return

        refs = gc.get_referrers(obj)
        refiter = iter(refs)
        self.ignore(refs, refiter)
        thisfile = sys._getframe().f_code.co_filename
        for ref in refiter:
            # Exclude all frames that are from this module or reftree.
            if isinstance(ref, FrameType) and ref.f_code.co_filename in (
                    thisfile, self.filename):
                continue

            # Exclude all functions and classes from this module or reftree.
            mod = getattr(ref, "__module__", "")
            if "django_dowser" in mod or "reftree" in mod or mod == '__main__':
                continue

            # Exclude all parents in our ignore list.
            if id(ref) in self._ignore:
                continue

            # Yield the (depth, id, repr) of our object.
            yield depth, 0, '%s<div class="branch">' % (" " * depth)
            if id(ref) in self.seen:
                yield depth, id(ref), "see %s above" % id(ref)
            else:
                self.seen[id(ref)] = None
                yield depth, id(ref), self.get_repr(ref, obj)

                for parent in self._gen(ref, depth + 1):
                    yield parent
            yield depth, 0, '%s</div>' % (" " * depth)

    def get_repr(self, obj, referent=None):
        """Return an HTML tree block describing the given object."""
        objtype = type(obj)
        typename = str(objtype.__module__) + "." + objtype.__name__
        prettytype = typename.replace("__builtin__.", "")

        name = getattr(obj, "__name__", "")
        if name:
            prettytype = "%s %r" % (prettytype, name)

        key = ""
        if referent:
            key = self.get_refkey(obj, referent)
        url = reverse('dowser_trace_object', args=(
            typename,
            id(obj)
        ))
        return ('<a class="objectid" href="%s">%s</a> '
                '<span class="typename">%s</span>%s<br />'
                '<span class="repr">%s</span>'
                % (url, id(obj), prettytype, key, get_repr(obj, 100))
                )

    def get_refkey(self, obj, referent):
        """Return the dict key or attribute name of obj which refers to
        referent."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if v is referent:
                    return " (via its %r key)" % k

        for k in dir(obj) + ['__dict__']:
            if getattr(obj, k, None) is referent:
                return " (via its %r attribute)" % k
        return ""
