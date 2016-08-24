<p><time>${today}</time></p>
<p>${_('{percent} of daily bandwidth of {size}').format(percent='{:.2f}%'.format(pct_capacity), size=h.hsize(capacity))}</p>
<p>
    ${ngettext('{count} candidate file', '{count} candidate files', count).format(count=count)}
    (${h.hsize(size)})
</p>
