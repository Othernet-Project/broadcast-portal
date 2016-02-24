<%inherit file='base.tpl'/>
<%namespace name="accepted_list" file="_accepted_list.tpl"/>
<%namespace name="review_list" file="_review_list.tpl"/>

<%block name="main">
    <div class="handles">
        <a class="handle" href="${url('queue_accepted')}" data-target="accepted">${_("Accepted")}</a>
        <a class="handle" href="${url('queue_review')}" data-target="review">${_("Review")}</a>
    </div>

    % if accepted is not UNDEFINED:
    <div class="queue accepted">
        ${accepted_list.body()}
    % else:
    <div class="queue accepted hidden">
    % endif
    </div>

    % if pending is not UNDEFINED:
    <div class="queue review">
        ${review_list.body()}
    % else:
    <div class="queue review hidden">
    % endif
    </div>
</%block>

<%block name="extra_body">
    <script type="text/template" id="queueLoadError">
        <p>${_('Queue loading failed. Please try again in a few seconds.')}</p>
    </script>
</%block>

<%block name="extra_scripts">
    <script src="${assets['js/queue']}"></script>
</%block>
