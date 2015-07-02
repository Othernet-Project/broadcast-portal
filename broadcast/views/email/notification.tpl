There are ${len(content)} new content broadcast and ${len(twitter)} new twitter broadcast requests.

% if content:
    List of content broadcast requests:
    % for item in content:
    ${host_url + url('scheduled_detail', item_type=item.type, item_id=item.id)}
    % endfor
% endif

% if twitter:
    List of twitter broadcast requests:
    % for item in twitter:
    ${host_url + url('scheduled_detail', item_type=item.type, item_id=item.id)}
    % endfor
% endif
