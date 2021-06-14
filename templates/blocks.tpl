% rebase('base', title='Blocks')

<h1>Blocks</h1>
<hr />

% blocks = system.all_blocks()
% services = sorted({ b.service for b in blocks if b.service.is_current })

<p>
  % for service in services:
    <a href="#{{service}}" class='button spaced-button'>{{ service }}</a>
  % end
</p>

% for service in services:
  % service_blocks = [block for block in blocks if block.service == service]

  <h2 id="{{service}}">{{ service }}</h2>

  % include('components/service_blocks', service=service, blocks=service_blocks)
% end
