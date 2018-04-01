import json

from rest_framework.renderers import JSONRenderer


class CoreJSONRenderer(JSONRenderer):
	charset = 'utf-8'
	object_label = 'object'

	def render(self, data, media_type=None, renderer_context=None):
		print("LALALA", data)
		if data.get('results', None) is not None:
			return json.dumps({
				self.pagination_object_label: data['results'],
				self.pagination_count_label: data['count']
			})

		elif data.get('errors', None) is not None:
			return super(CoreJSONRenderer, self).render(data)

		else:
			return json.dumps({
				self.object_label: data
			})

# {
# 	data:{
# 		....
# 	},
# 	error:{
# 		....
# 	},
# 	error_msg:{
# 		....
# 	}
# }
