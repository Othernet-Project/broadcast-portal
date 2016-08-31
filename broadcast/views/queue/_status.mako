<h2><time class="date" datetime="${today}">${_('{date} filecast queue').format(date=today)}</time></h2>
<p class="capacity">
    <span class="capacity-gauge-outer">
        <span class="capacity-gauge-inner" style="width: ${pct_capacity}%"></span>
    </span>
    ${_('{percent} of {size}/day').format(percent='{:.2f}%'.format(pct_capacity), size=h.hsize(capacity))}
</p>
<p>
    ${ngettext('{count} candidate file', '{count} candidate files', count).format(count=count)}
    (${h.hsize(size)})
</p>
%if request.is_xhr:
<p>
    <a class="button" href="${url('queue:status')}" class="button">
        ${_('See full status')}
    </a>
</p>
%endif
